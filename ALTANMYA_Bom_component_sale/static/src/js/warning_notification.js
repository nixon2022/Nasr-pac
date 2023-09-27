    odoo.define('ALTANMYA_Bom_component_sale.warning', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');
    var session = require('web.session');
//    var framework = require('web.framework');

    var _t = core._t;
    var d3 = window.d3;

    publicWidget.registry.Warning = publicWidget.Widget.extend({

            selector: '#js_warning',
            events: {
                'click .o_alert_warning_js': '_onCloseButtonClick',
            },

            start: async function() {
            console.log("heloo from warning");

            },

            _onCloseButtonClick: function () {
                console.log("heloo from warning");
            // Assuming you want to hide the parent div when the close button is clicked
            //$(event.currentTarget).closest('.alert.alert-danger').hide();
            },

    });
});

