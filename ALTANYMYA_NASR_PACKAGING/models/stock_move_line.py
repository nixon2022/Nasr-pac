from odoo import api, fields, models


class StockMoveLineNasr(models.Model):
    _inherit = 'stock.move.line'

    pallet = fields.Integer(string="Pallet Number", default=1)
    delivery_date = fields.Datetime("Delivery Date", compute='_compute_delivery_date')
    No_of_carton = fields.Integer(string="No. of Carton")
    No_of_pcs = fields.Integer(string="No. of Pcs.")
    job_ticket_id = fields.Many2one('mrp.production', string='Job Ticket', compute='_compute_job_ticket_id')

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
                        [('order_id', 'in', self.move_id.picking_id.sale_id.ids), ('product_id', '=', rec.product_id.id)])
                    if len(line_order) > 1:
                        job_ticket = self.env['mrp.production'].search(
                            [('product_id', '=', rec.product_id.id), ('origin', '=', rec.move_id.picking_id.group_id.name)])
                        print('job', job_ticket)
                        print('line', line_order)
                        # for i in range(len(job_ticket)):
                        #     if job_ticket[i].id == rec.id:
                        #         print(rec.id)
                        #         print(job_ticket[i], i)
                        #         print(line_order[i], i)
                        #         rec.job_ticket_id = job_ticket[i]


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
