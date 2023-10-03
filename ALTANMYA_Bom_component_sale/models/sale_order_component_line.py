from odoo import api, fields, models, tools, _


class SaleOrderComponent(models.Model):
    _name = "sale.order.component"
    _description = "Sale Order Component"


    bom_order_line = fields.Many2one('sale.order.line', string="Product",domain=[],copy=False,required=True)
    bom_id = fields.Many2one('mrp.bom',copy=False)
    new_product = fields.Many2one('product.product', string='Components',copy=False,required=True)
    new_quan = fields.Float(string='Quantity',copy=False,required=True)
    order_line_from_parent = fields.Many2one('product.product', string='Product',copy=False,required=True)
    edited_component = fields.Boolean(string="ed",copy=False)
    new_uom = fields.Many2one('uom.uom', string='Uom',copy=False,required=True)
    new_uom_related = fields.Many2one('uom.uom', string='Uom',copy=False,required=True,compute='_compute_new_uom')
    new_forecast = fields.Float( string='Forecast Quantity',copy=False,compute='_compute_new_forecast',required=True,readonly=True)
    new_related = fields.Char( string=' Availability',default='',copy=False,compute='_compute_new_related',readonly=True)
    reserved_quan= fields.Float( string=' Reserved Quantity',copy=False , compute='_compute_reserved')


    line_quantity= fields.Float(string="new quantity line ")
    component_quantity= fields.Float(string="new quantity component ")
    bom_quantity= fields.Float(string="new bom component ")

    @api.onchange('new_product')
    def new_uom_in_line(self):
        for rec in self:
            rec.new_uom=rec.new_uom_related


    @api.depends('new_product')
    def _compute_new_uom(self):
        for record in self:
            record.new_uom_related = record.new_product.uom_id.id


    @api.depends('new_product')
    def _compute_new_forecast(self):
        for record in self:
            record.new_forecast = record.new_product.virtual_available

    @api.depends('new_forecast', 'new_quan')
    def _compute_reserved(self):
        for record in self:
            record.reserved_quan = record.new_forecast - record.new_quan


    @api.depends('new_forecast', 'new_quan')
    def _compute_new_related(self):
        for record in self:
            if record.new_forecast < record.new_quan:
                record.new_related = "Not Available"
            else:
                record.new_related = "Available "

    @api.onchange('new_quan', 'new_product')
    def on_change_component(self):
        if self.new_quan or self.new_product:
            self.edited_component = True

    @api.onchange('new_product')
    def on_change_new_product(self):
        if self.new_product:

            active_record_id = self.env.context.get('active_id', False)
            if active_record_id:
                sale_order = self.env['sale.order'].browse(active_record_id)
                sale_order_lines = sale_order.order_line
                return {'domain': {'bom_order_line': [('id', 'in', sale_order_lines.ids)]}}
        return {'domain': {'bom_order_line': []}}

    @api.onchange('bom_order_line')
    def on_change_bom_order_line(self):
        if self.bom_order_line:
            self.order_line_from_parent = self.bom_order_line.product_id
        else:
            self.order_line_from_parent = None

    @api.onchange('new_product')
    def onchange_template_id(self):
        res = {}
        if self.new_product:
            self.new_forecast = self.new_product.virtual_available
        if res:

            return res

    # def unlink(self):
    #
    #     self.bom_order_line.order_id.compute_bool = True
    #
    #     return super(SaleOrderComponent, self).unlink()
