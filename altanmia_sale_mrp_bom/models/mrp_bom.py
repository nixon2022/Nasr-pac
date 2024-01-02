# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
        required=True, readonly=False, tracking=True)

    from_sale = fields.Boolean('Form sale', compute="_compute_from_sale")

    unit_cost = fields.Float("Unit Cost", compute="_compute_unit_cost", readonly=False, store=True)
    sale_qty = fields.Float("Sale Quantity", compute="_compute_sale_qty")
    origin = fields.Boolean("Origin", store=False, default=lambda self: self.sequence == 1)
    create_as_new = fields.Boolean("Save As New", store=False, default=False)

    # add tracking

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        check_company=True, index=True, tracking=True,
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True)
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        check_company=True, index=True, tracking=True,
        domain="['&', ('product_tmpl_id', '=', product_tmpl_id), ('type', 'in', ['product', 'consu']),  '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If a product variant is defined the BOM is available only for this product.")

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

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        if vals.get("origin", False):
            res.write({'origin': True})
        return res

    def write(self, vals):
        product = self.product_id if self.product_id else self.product_tmpl_id.product_variant_id
        domain = self._bom_find_domain(product,
                                       bom_type='normal')
        boms = self.search(domain, order='sequence')

        # if create_as_new in vals or default_create_as_new in context
        if vals.get("create_as_new", self._context.get('default_create_as_new', False)):
            code = vals.get('code', False)
            if not code:
                code = self.get_code()
                if code:
                    vals['code'] = code

            vals['create_as_new'] = False

            vals['sequence'] = len(boms) + 1
            new_obj = self.copy()
            res = super(MrpBom, self).write(vals)
        else:
            res = super(MrpBom, self).write(vals)

        if vals.get("origin", False):
                sequence = 2
                for bom in boms:
                    if bom.id == self.id:
                        bom.write({'sequence': 1})
                    else:
                        bom.write({'sequence': sequence})
                        sequence += 1
        return res

    def get_code(self):
        if self.product_tmpl_id:
            domain = [('product_tmpl_id', '=', self.product_tmpl_id.id)]
            number_of_bom_of_this_product = self.env['mrp.bom'].search_count(domain)
            if number_of_bom_of_this_product:  # add a reference to the bom if there is already a bom for this product
                return _("%s (new) %s", self.product_tmpl_id.name, number_of_bom_of_this_product)

        return False


class MrpBomLine(models.Model):
    _name = 'mrp.bom.line'
    _inherit = ['mrp.bom.line', "mail.thread", "mail.activity.mixin"]

    forecast_availability = fields.Float('Forecast Availability', compute='_compute_forecast_information',
                                         digits='Product Unit of Measure', compute_sudo=True)
    available = fields.Float('Available', compute='_compute_forecast_information')
    qty_needed = fields.Float('Needed QTY', compute='_compute_forecast_information')

    from_sale = fields.Boolean(related='bom_id.from_sale')

    # add tracking to this fields
    product_id = fields.Many2one('product.product', 'Component', required=True, check_company=True, tracking=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id',
                                      store=True, index=True, tracking=True)
    company_id = fields.Many2one(
        related='bom_id.company_id', store=True, index=True, readonly=True, tracking=True)
    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits='Product Unit of Measure', required=True, tracking=True)

    @api.depends('product_id', 'product_qty', 'bom_id.sale_qty')
    def _compute_forecast_information(self):
        for record in self:
            # Check if the product is available based on a product_qty
            needed_quantity = record.product_qty * (record.bom_id.sale_qty or 1) / (record.bom_id.product_qty or 1)
            record.forecast_availability = record.product_id.virtual_available - needed_quantity + record.product_qty
            record.qty_needed = needed_quantity
            record.available = record.product_id.virtual_available

    def _message_log(self, *, body='', author_id=None, email_from=None, subject=False, message_type='notification',
                     **kwargs):
        self.bom_id._message_log(
            body=f"line {self.display_name}({self.product_qty}): {body}", subject=subject, message_type=message_type,
            **kwargs
        )
        return super(MrpBomLine, self)._message_log(**kwargs)

    @api.model
    def create(self, vals):
        res = super(MrpBomLine, self).create(vals)
        message = "Created"
        res._message_log(body=message)
        return res

    def unlink(self):
        for line in self:
            message = "Deleted"
            line._message_log(body=message)
        return super(MrpBomLine, self).unlink()
