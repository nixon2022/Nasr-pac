/* global AdyenCheckout */
odoo.define('payment_hyperpay.payment_form', require => {
    'use strict';

    const core = require('web.core');
    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const _t = core._t;

    const hyperpayMixin = {

        _prepareTransactionRouteParams: function (provider, paymentOptionId, flow) {
            var params = this._super(...arguments);
            if (provider !== 'hyperpay') {
                return params
            }else{
                const pway = this.$('input[name=payment_way]:checked').val();
                params['payment_way'] =  pway;
                return params
            }
        },
    };

    checkoutForm.include(hyperpayMixin);
    manageForm.include(hyperpayMixin);

    var publicWidget = require('web.public.widget');

    publicWidget.registry.hyperpay = publicWidget.Widget.extend({
        selector: '.o_payment_form',

        events: {
            'change .checkbox-input': '_onPaymentWayChanged',
        },
        _onPaymentWayChanged : function(ev){
            const $pway = this.$('input[name=payment_way]:checked');
            const $checkoo = $pway.closest('.card-footer').children().last();
            if( $checkoo.hasClass("clearfix"))
            {
                return;
            }
            if ($pway.val() == 'stc_pay' || $pway.val() == 'apple_pay'){
                $checkoo.addClass('d-none');
            }else{
                $checkoo.removeClass('d-none');
            }
        }
    });
});
