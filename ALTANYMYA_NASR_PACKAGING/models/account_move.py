from odoo import models, fields, api
from num2words import num2words


class AcountMoveNasr(models.Model):
    _inherit = 'account.move'

    Total_quantity_ordered = fields.Char(string="Total_quantity_ordered", compute='_get_value', store=True)
    total_price_words = fields.Char(string="Total Price in English Words", compute='_get_value')
    total_price_words_arabic = fields.Char(string="Total Price in Arabic Words", compute='_get_value')
    delivery_id = fields.Many2one('stock.picking', compute="_compute_delivery_id")
    bank_details = fields.Html(string="Bank Details")

    def _compute_delivery_id(self):
        for rec in self:
            rec.delivery_id = None
            if rec.invoice_origin:
                deliveries = self.env['stock.picking'].search([('origin', '=', rec.invoice_origin),
                                                               ('location_dest_id.usage', '=', 'customer')])
                print('del', deliveries)
                for delivery in deliveries:
                    if delivery.date_done.date() == rec.l10n_sa_delivery_date:
                        rec.delivery_id = delivery
                # for delivery in deliveries:
                #     if delivery.location_dest_id.usage == 'customer':
                


    @api.depends('invoice_line_ids.quantity')
    def _get_value(self):
        for order in self:
            qty = 0
            for line in order.invoice_line_ids:
                qty += line.quantity
            order.Total_quantity_ordered = str(qty)

            currency_symbol = order.currency_id.currency_unit_label or ''
            subcurrency_symbol = order.currency_id.currency_subunit_label or ''

            currency_symbol_arabic = order.currency_id.unit_arabic or ''
            subcurrency_symbol_arabic = order.currency_id.subunit_arabic or ''

            total_price_words = num2words(float(order.amount_total), lang='en').title()
            if 'Point' in total_price_words:
                total_price_words = total_price_words.split('Point')
                order.total_price_words = f"{total_price_words[0]} {currency_symbol} & {total_price_words[1]} {subcurrency_symbol}"
            else:
                order.total_price_words = f"{total_price_words} {currency_symbol}"

            total_price_words_arabic = num2words(float(order.amount_total), lang='ar').title()
            if 'فاصلة' in total_price_words_arabic:
                total_price_words_arabic = total_price_words_arabic.split('فاصلة')
                order.total_price_words_arabic = f"{total_price_words_arabic[0]} {currency_symbol_arabic} و {total_price_words_arabic[1]} {subcurrency_symbol_arabic} فقط "
            else:
                order.total_price_words_arabic = f"{total_price_words_arabic} {currency_symbol_arabic} فقط "
