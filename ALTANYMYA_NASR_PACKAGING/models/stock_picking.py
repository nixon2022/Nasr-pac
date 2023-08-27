from odoo import api, fields, models, _
from datetime import datetime


class StockPickingNasr(models.Model):
    _inherit = 'stock.picking'
    random_unique_number = fields.Char(string='Random Unique Number', compute='_compute_random_unique_number')
    partial_delivery = fields.Char(string='Partial Delivery', compute='_compute_partial_delivery')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_sale_order_id')
    delivery_date_per_item_done = fields.Datetime("Delivery Date")
    plate_number = fields.Char(string='Plate No.')
    driver = fields.Char(string='Driver')
    mobile_number = fields.Char(string='Mobile No.')
    transporter = fields.Many2one('res.partner', string='Transporter')
    remarks = fields.Html(string="Remarks")
    lot_ids = fields.Many2one('stock.production.lot', string="Lot Serial/Number", compute="_compute_lot_id")
    lot_id_name = fields.Char(string="Lot Serial/Number")

    def _compute_lot_id(self):
        for rec in self:
            elif rec.group_id and rec.partial_delivery and rec.product_id.tracking != 'lot':
                lot_name = 'NASP' + rec.group_id.name[-7:] + rec.partial_delivery
                rec.lot_id_name = lot_name
                rec.lot_ids = None

            elif not rec.group_id and rec.partial_delivery and rec.product_id.tracking != 'lot':
                lot_name = 'NASP' + rec.partial_delivery
                rec.lot_id_name = lot_name
                rec.lot_ids = None

            else:
                rec.lot_ids = None

    def button_validate(self):
        for rec in self:
            now = datetime.now()
            rec.delivery_date_per_item_done = now.strftime('%Y-%m-%d %H:%M:%S')
        return super(StockPickingNasr, self).button_validate()

    @api.depends('origin')
    def _compute_sale_order_id(self):
        for rec in self:
            rec.sale_order_id = None
            if rec.origin:
                rec.sale_order_id = rec.env['sale.order'].search([('name', '=', rec.origin)])

    @api.depends('backorder_id')
    def _compute_partial_delivery(self):
        for rec in self:
            rec.partial_delivery = '001'
            counter = 0
            found_backorders = rec.env['stock.picking'].search([('origin', '=', rec.origin)])
            if found_backorders:
                if rec.backorder_id:
                    backorderseq = rec.backorder_id
                    for back_orders in found_backorders:
                        if backorderseq.id == back_orders.id:
                            counter += 1
                            backorderseq = back_orders.backorder_id
                if len(str(counter)) == 1:
                    if counter == 0:
                        rec.partial_delivery = '001'
                    else:
                        rec.partial_delivery = '00' + str(counter + 1)
                if len(str(counter)) == 2:
                    rec.partial_delivery = '0' + str(counter + 1)
                if len(str(counter)) == 3:
                    rec.partial_delivery = str(counter + 1)

    def _compute_random_unique_number(self):
        for rec in self:
            rec.random_unique_number = 1137356748381521741 + rec.id
            rec.random_unique_number = '(00)' + rec.random_unique_number[-17:]


class StockPickingTypeNasr(models.Model):
    _inherit = 'stock.picking.type'

    generate_lot_id_nasr = fields.Boolean(string="Generate New Lot/Serial Number on Delivery")