from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('name')
    def set_domain_for_product(self):
        product_ids = self.env['product.product'].search(['|', ('customer', '=', self.order_id.partner_id.id),
                                                               ('for_all_customers', '=', True)]).ids
        res = {}
        res['domain'] = {'product_id': [('id', 'in', product_ids),
                                        ('sale_ok', '=', True), '|',
                                        ('company_id', '=', False),
                                        ('company_id', '=', self.company_id.id)]}
        return res

    product_id = fields.Many2one(
        'product.product', string='Product',
        change_default=True, ondelete='restrict', check_company=True)
