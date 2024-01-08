# Copyright 2020 Akretion Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="BoM",
        domain="[('product_tmpl_id.product_variant_ids', '=', product_id),"
               "'|', ('product_id', '=', product_id), "
               "('product_id', '=', False)]",
    )

    @api.constrains("bom_id", "product_id")
    def _check_match_product_variant_ids(self):
        for line in self:
            if line.bom_id:
                bom_product_tmpl = line.bom_id.product_tmpl_id
                bom_product = bom_product_tmpl.product_variant_ids
            else:
                bom_product_tmpl, bom_product = None, None
            line_product = line.product_id
            if not bom_product or line_product == bom_product:
                continue
            raise ValidationError(
                _(
                    "Please select BoM that has matched product with the line `{}`"
                ).format(line_product.name)
            )

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            bom = self.env['mrp.bom']._bom_find(rec.product_id, bom_type='normal').get(rec.product_id)
            rec.bom_id = bom or None

    @api.onchange('bom_id')
    def onchange_bom(self):
        for record in self:
            record.product_uom_qty = record.bom_id.sale_qty or record.product_uom_qty
            record.price_unit = record.bom_id.unit_cost or record.price_unit
