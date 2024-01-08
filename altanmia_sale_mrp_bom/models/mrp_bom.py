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
        bom = self.env['mrp.bom']._bom_find(prod_id, bom_type='normal').get(prod_id)

        if not bom:
            return []

        # Prepare the BOM lines for the default values
        bom_lines = [(0, 0, {
            'product_id': line.product_id.id,
            'product_qty': line.product_qty,
            'product_uom_id': line.product_uom_id.id,
        }) for line in bom.bom_line_ids]

        return bom_lines

    def _get_default_product_qty(self):
        prod_id = self._context.get('default_product_id', False)
        if not prod_id:
            return 1
        prod_id = self.env['product.product'].browse(prod_id)

        # Find the Bill of Materials (BOM) for the product
        bom = self.env['mrp.bom']._bom_find(prod_id, bom_type='normal').get(prod_id)

        return bom.product_qty if bom else 1

    bom_line_ids = fields.One2many('mrp.bom.line', 'bom_id', 'BoM Lines', default=_get_default_bom_line_id, copy=True)

    product_qty = fields.Float(
        'Quantity',
        digits='Product Unit of Measure',
        default=_get_default_product_qty,
        required=True, readonly=False)

    from_sale = fields.Boolean('Form sale', compute="_compute_from_sale")

    unit_cost = fields.Float("Unit Cost", compute="_compute_unit_cost", readonly=False, store=True)
    sale_qty = fields.Float("Sale Quantity", compute="_compute_sale_qty")

    def _compute_from_sale(self):
        for rec in self:
            rec.from_sale = self._context.get('default_from_sale', rec.from_sale)

    def _compute_sale_qty(self):
        for rec in self:
            rec.sale_qty = self._context.get('default_sale_qty', rec.sale_qty)

    @api.depends('bom_line_ids', 'product_qty')
    def _compute_unit_cost(self):
        for rec in self:
            total = 0
            for line in rec.bom_line_ids:
                total += line.product_id.list_price * line.product_qty / rec.product_qty
            rec.unit_cost = total

    def write(self, vals):
        print("write vales", vals)
        if self.env.context.get("create_new", False):
            code = vals.get('code', False)
            if not code:
                code = self.get_code()
                if code:
                    vals['code'] = code
            if vals.get('bom_line_ids', False):
                create_lines = [line for line in vals.get('bom_line_ids', []) if line[0] == 0]
                for line in [line for line in vals.get('bom_line_ids', []) if line[0] in [4, 1]]:
                    origin_line = self.bom_line_ids.filtered(lambda x: x.id == line[1])
                    values = {
                        'product_id': origin_line.product_id.id,
                        'product_qty': origin_line.product_qty,
                        'product_uom_id': origin_line.product_uom_id.id,
                    }
                    if line[0] == 1:
                        values.update(line[2])
                    line = (0, 0, values)
                    create_lines.append(line)
                vals['bom_line_ids'] = create_lines

            new_rec = self.copy(default=vals)
            return new_rec
        else:
            return super(MrpBom, self).write(vals)

    def get_code(self):
        if self.product_tmpl_id:
            domain = [('product_tmpl_id', '=', self.product_tmpl_id.id)]
            number_of_bom_of_this_product = self.env['mrp.bom'].search_count(domain)
            if number_of_bom_of_this_product:  # add a reference to the bom if there is already a bom for this product
                return _("%s (new) %s", self.product_tmpl_id.name, number_of_bom_of_this_product)

        return False


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    forecast_availability = fields.Float('Forecast Availability', compute='_compute_forecast_information',
                                         digits='Product Unit of Measure', compute_sudo=True)
    available = fields.Float('Available', compute='_compute_forecast_information')
    qty_needed = fields.Float('Needed QTY', compute='_compute_forecast_information')

    from_sale = fields.Boolean(related='bom_id.from_sale')

    @api.depends('product_id', 'product_qty', 'bom_id.sale_qty')
    def _compute_forecast_information(self):
        for record in self:
            # Check if the product is available based on a product_qty
            needed_quantity = record.product_qty * (record.bom_id.sale_qty or 1) / (record.bom_id.product_qty or 1)
            record.forecast_availability = record.product_id.virtual_available - needed_quantity
            record.qty_needed = needed_quantity
            record.available = record.product_id.virtual_available
