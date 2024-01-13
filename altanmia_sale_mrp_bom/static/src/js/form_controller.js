odoo.define('altanmia_sale_mrp_bom.FormController', function (require) {
    /**
     * Monkeypatching of the form controller to modify the behaviour
     * of buttons in form views so the that Studio Validation
     * mechanism works with them.
     *
     * Intercept calls to `_callButtonAction` and do a proper validation
     * of approvals before continuing with the action.
     */
    'use strict';

    const core = require('web.core');
    const FormController = require('web.FormController');
    const BasicModel = require('web.BasicModel')

    const _t = core._t;

    FormController.include({
        /**
         * Intercept calls for buttons that have the `studio_approval` attrs
         * set; the action (method or action id) is checked server-side for the
         * current record to check if the current user can proceed or not base on
         * approval flows. If not, a notification is displayed detailing the issue;
         * if yes, the action proceeds normally.
         * @override
         * @param {Object} attrs the attrs of the button clicked
         * @param {Object} [record] the current state of the view
         * @returns {Promise}
         */
        async _onButtonClicked(ev) {
            // stop the event's propagation as a form controller might have other
            // form controllers in its descendants (e.g. in a FormViewDialog)
            ev.stopPropagation();
            var self = this;
            var def;

            this._disableButtons();


            var attrs = ev.data.attrs;
            const record = ev.data.record;
            const btnContext = record.getContext({additionalContext: attrs.context || {}});

            function saveAndExecuteAction () {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                    additionalContext: btnContext
                }).then(function () {
                    // we need to re-get the record to make sure we have changes made
                    // by the basic model, such as the new res_id, if the record is
                    // new.

                    var record = self.model.get(ev.data.record.id);
                    return self._callButtonAction(attrs, record);
                });
            }
            if (attrs.confirm) {
                def = new Promise(function (resolve, reject) {
                    Dialog.confirm(self, attrs.confirm, {
                        confirm_callback: saveAndExecuteAction,
                    }).on("closed", null, resolve);
                });
            } else if (attrs.special === 'cancel') {
                def = this._callButtonAction(attrs, ev.data.record);
            } else if (!attrs.special || attrs.special === 'save') {
                // save the record but don't switch to readonly mode
                def = saveAndExecuteAction();
            } else {
                console.warn('Unhandled button event', ev);
                return;
            }

            // Kind of hack for FormViewDialog: button on footer should trigger the dialog closing
            // if the `close` attribute is set
            def.then(function () {
                self._enableButtons();
                if (attrs.close) {
                    self.trigger_up('close_dialog');
                }
            }).guardedCatch(this._enableButtons.bind(this));
        },
        async _saveRecord(recordID, options) {
            recordID = recordID || this.handle;
            options = _.defaults(options || {}, {
                stayInEdit: false,
                reload: true,
                savePoint: false,
            });


            // Check if the view is in a valid state for saving
            // Note: it is the model's job to do nothing if there is nothing to save
            if (this.canBeSaved(recordID)) {
                var self = this;
                var saveDef = this.model.save(recordID, { // Save then leave edit mode
                    reload: options.reload,
                    savePoint: options.savePoint,
                    viewType: options.viewType,
                    additionalContext: options.additionalContext
                });
                if (!options.stayInEdit) {
                    saveDef = saveDef.then(function (fieldNames) {
                        var def = fieldNames.length ? self._confirmSave(recordID) : self._setMode('readonly', recordID);
                        return def.then(function () {
                            return fieldNames;
                        });
                    });
                }
                return saveDef;
            } else {
                return Promise.reject("SaveRecord: this.canBeSave is false"); // Cannot be saved
            }
        },
    });

    BasicModel.include({
        save: function (recordID, options) {
            var self = this;
            function _save() {
                options = options || {};
                var record = self.localData[recordID];
                if (options.savePoint) {
                    self._visitChildren(record, function (rec) {
                        var newValue = rec._changes || rec.data;
                        if (newValue instanceof Array) {
                            rec._savePoint = newValue.slice(0);
                        } else {
                            rec._savePoint = _.extend({}, newValue);
                        }
                    });

                    // save the viewType of edition, so that the correct readonly modifiers
                    // can be evaluated when the record will be saved
                    for (let fieldName in (record._changes || {})) {
                        record._editionViewType[fieldName] = options.viewType;
                    }
                }
                var shouldReload = 'reload' in options ? options.reload : true;
                var method = self.isNew(recordID) ? 'create' : 'write';
                if (record._changes) {
                    // id never changes, and should not be written
                    delete record._changes.id;
                }
                var changes = self._generateChanges(record, {viewType: options.viewType, changesOnly: method !== 'create'});

                // id field should never be written/changed
                delete changes.id;

                if (method === 'create') {
                    var fieldNames = record.getFieldNames();
                    _.each(fieldNames, function (name) {
                        if (changes[name] === null) {
                            delete changes[name];
                        }
                    });
                }

                var prom = new Promise(function (resolve, reject) {
                    var changedFields = Object.keys(changes);

                    if (options.savePoint) {
                        resolve(changedFields);
                        return;
                    }

                    // in the case of a write, only perform the RPC if there are changes to save
                    if (method === 'create' || changedFields.length) {
                        var args = method === 'write' ? [[record.data.id], changes] : [changes];
                        self._rpc({
                                model: record.model,
                                method: method,
                                args: args,
                                context: record.getContext(options),
                            }).then(function (id) {
                                if (method === 'create') {
                                    record.res_id = id;  // create returns an id, write returns a boolean
                                    record.data.id = id;
                                    record.offset = record.res_ids.length;
                                    record.res_ids.push(id);
                                    record.count++;
                                }

                                var _changes = record._changes;

                                // Erase changes as they have been applied
                                record._changes = {};

                                // Optionally clear the DataManager's cache
                                self._invalidateCache(record);

                                self.unfreezeOrder(record.id);

                                // Update the data directly or reload them
                                if (shouldReload) {
                                    self._fetchRecord(record).then(function () {
                                        resolve(changedFields);
                                    });
                                } else {
                                    _.extend(record.data, _changes);
                                    resolve(changedFields);
                                }
                            }).guardedCatch(reject);
                    } else {
                        resolve(changedFields);
                    }
                });
                prom.then(function () {
                    self._updateDuplicateRecords(record.id, (id) => {
                        Object.assign(self.localData[id].data, record.data);
                    });
                    record._isDirty = false;
                });
                return prom;
            }
            if (this.bypassMutex) {
                return _save();
            } else {
                return this.mutex.exec(_save);
            }
        },
    });
});
