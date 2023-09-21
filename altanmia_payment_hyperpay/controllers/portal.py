from odoo.addons.payment.controllers import portal as payment_portal

class PaymentPortal(payment_portal.PaymentPortal):

    def _create_transaction(
            self, payment_option_id, reference_prefix, amount, currency_id, partner_id, flow,
            tokenization_requested, landing_route, is_validation=False, invoice_id=None,
            custom_create_values=None, **kwargs):

        if kwargs.get('payment_way',False):
            custom_create_values['payment_way'] = kwargs.pop('payment_way')

        tx = super(PaymentPortal, self)._create_transaction(payment_option_id, reference_prefix, amount,
                                                                   currency_id, partner_id, flow,
                                                                   tokenization_requested, landing_route, is_validation,
                                                                   invoice_id,
                                                                   custom_create_values, **kwargs)

        return tx


