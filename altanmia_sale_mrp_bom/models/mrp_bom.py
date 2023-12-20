# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv.expression import AND, NEGATIVE_TERM_OPERATORS
from odoo.tools import float_round

from collections import defaultdict


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    def _get_default_bom_line_id(self):
        prod_id = self._context.get('default_product_id', False)
        if not prod_id:
            return []
        prod_id = self.env['product.product'].browse(prod_id)

        # Find the Bill of Materials (BOM) for the product
        bom = self.env['mrp.bom']._bom_find(prod_id, picking_type=self.picking_type_id, bom_type='normal').get(prod_id)

        if not bom:
            return []

        # Prepare the BOM lines for the default values
        bom_lines = [(0, 0, {
            'product_id': line.product_id.id,
            'product_qty': line.product_qty,
            'product_uom_id': line.product_uom_id.id,
        }) for line in bom.bom_line_ids]

        return bom_lines

    def _get_default_total_cost(self):
        for record in self:
            total = 0
            for line in record.bom_line_ids:
                total += line.product_id.list_price * line.product_qty
            record.unit_cost = total

    bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id', 'BoM Lines', default=_get_default_bom_line_id, copy=True)

    sale_qty = fields.Integer("Sale Quantity")

    from_sale = fields.Boolean('Form sale', default=False)

    unit_cost = fields.Float("Unit Cost", default=_get_default_total_cost)

    @api.onchange('bom_line_ids')
    def _on_bom_line_change(self):
        for record in self:
            total = 0
            for line in record.bom_line_ids:
                total += line.product_id.list_price * line.product_qty
            record.unit_cost = total


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    forecast_availability = fields.Float('Forecast Availability', compute='_compute_forecast_information',
                                         digits='Product Unit of Measure', compute_sudo=True)

    from_sale = fields.Boolean(related='bom_id.from_sale')

    @api.depends('product_id', 'product_qty', 'bom_id.sale_qty')
    def _compute_forecast_information(self):
        for record in self:
            total_quantity_available = record.product_id.virtual_available
            # Check if the product is available based on a threshold
            availability_threshold = record.product_qty * record.bom_id.sale_qty
            record.forecast_availability = total_quantity_available - availability_threshold