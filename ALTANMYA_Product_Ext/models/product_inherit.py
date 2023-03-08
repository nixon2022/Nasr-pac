from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    customer = fields.Many2one('res.partner', string="Customer")
    for_all_customers = fields.Boolean(string="Make This Product For All Customers",
                                       default=False)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    customer = fields.Many2one('res.partner',
                               related='product_tmpl_id.customer',
                               string="Customer",
                               readonly=False)
    for_all_customers = fields.Boolean(string="Make This Product For All Customers",
                                       related='product_tmpl_id.for_all_customers',
                                       readonly=False)
