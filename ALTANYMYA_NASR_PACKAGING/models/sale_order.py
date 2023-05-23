from odoo import fields, models, api


class SaleOrderNasr(models.Model):
    _inherit = 'sale.order'

    to_ID = fields.Many2one('res.partner', string="To")
    received_on = fields.Datetime(string="Received on")
    p_o = fields.Datetime(string="Dated")
    new_commitment_date = fields.Datetime(string="new_commitment_date", compute='_compute_new_commitment_date')

    @api.depends('order_line')
    def _compute_new_commitment_date(self):
        for rec in self:
            if rec.order_line:
                com_date = []
                for line in rec.order_line:
                    if line.delivery_date_sale_order_line:
                        com_date.append(line.delivery_date_sale_order_line)
                if com_date:
                    rec.new_commitment_date = max(com_date)
                    rec.commitment_date = max(com_date)
                else:
                    rec.new_commitment_date = None
            else:
                rec.new_commitment_date = None

