from odoo import api, fields, models


class StockMoveLineNasr(models.Model):
    _inherit = 'stock.move.line'

    pallet = fields.Integer(string="Pallet Number", default=1)
    delivery_date = fields.Datetime("Delivery Date", compute='_compute_delivery_date')
    No_of_carton = fields.Integer(string="No. of Carton")
    No_of_pcs = fields.Integer(string="No. of Pcs.")
    job_ticket_id = fields.Many2one('mrp.production', string='Job Ticket', compute='_compute_job_ticket_id')

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('product_id'):
            default['No_of_carton'] = default['product_id'].No_of_carton
            default['No_of_pcs'] = default['product_id'].No_of_pcs
            default['lot_id'] = default['product_id'].lot_id

        return super(StockMoveLineNasr, self).copy(default)

    @api.model
    def create(self, vals):
        res = super(StockMoveLineNasr, self).create(vals)
        res['No_of_carton'] = res['product_id'].No_of_carton
        res['No_of_pcs'] = res['product_id'].No_of_pcs
        if res['move_id'].picking_id.group_id:
            if res['product_id'].tracking == 'lot':
                if res['move_id'].picking_id.picking_type_id.generate_lot_id_nasr:
                    lot_name = "NASP" + res['move_id'].picking_id.group_id.name[-7:] + res['move_id'].picking_id.partial_delivery
                    lot_exist = self.env['stock.production.lot'].search([('name', '=', lot_name)])
                    if not lot_exist:
                        lot_id = self.env['stock.production.lot'].create({
                            'name': lot_name,
                            'product_id': res['product_id'].id,
                            # 'product_qty': res['product_id'].product_qty,
                            'company_id': res['company_id'].id,
                        })
                        res['lot_id'] = lot_id
                    else:
                        res['lot_id'] = lot_exist
        return res

    @api.depends('picking_id')
    def _compute_job_ticket_id(self):
        for rec in self:
            rec.job_ticket_id = None
            if rec.origin:
                result = rec.env['mrp.production'].search([('name', '=', rec.picking_id.group_id.name)])
                if result:
                    rec.job_ticket_id = result
                else:
                    rec.job_ticket_id = rec.move_id.sale_line_id.manufacturing_order_id

                    line_order = self.env['sale.order.line'].search(
                        [('order_id', 'in', self.move_id.picking_id.sale_id.ids),
                         ('product_id', '=', rec.product_id.id)])
                    if len(line_order) > 1:
                        job_ticket = self.env['mrp.production'].search(
                            [('product_id', '=', rec.product_id.id),
                             ('origin', '=', rec.move_id.picking_id.group_id.name)])
                        for i in range(len(job_ticket)):
                            if job_ticket[i].sale_order_line_id == rec.move_id.sale_line_id:
                                rec.job_ticket_id = job_ticket[i]

    @api.depends('move_id')
    def _compute_delivery_date(self):
        for rec in self:
            if rec.move_id:
                if rec.product_id == rec.move_id.product_id:
                    rec.delivery_date = rec.move_id.delivery_date_per_item
                else:
                    rec.delivery_date = None
            else:
                rec.delivery_date = None
