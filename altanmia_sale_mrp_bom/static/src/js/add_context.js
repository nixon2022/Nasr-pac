odoo.define('altanmia_sale_mrp_bom.add_context', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var Session = require('web.session');

var QWeb = core.qweb;

console.info("model model");
var addContext = AbstractAction.extend({
    events: {
        "click .save_as_new": function() {
            console.info("calles");
            this.do_action('mrp.mrp_bom_form_action', {
                additional_context: {'new_one': true},
            });
        },
    }
    });
    core.action_registry.add('altanmia_sale_mrp_bom_add_context', addContext);

    return addContext;
});