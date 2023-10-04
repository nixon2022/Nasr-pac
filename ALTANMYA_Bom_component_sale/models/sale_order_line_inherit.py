from odoo.tools import copy

from odoo import api, fields, models, tools, _


class saleorder(models.Model):
    _inherit = "sale.order"

    component = fields.Many2many('sale.order.component', string='order', copy=False)
    component_compute = fields.Boolean(compute='_compute_component')
    compute_bool = fields.Boolean(string='bool', copy=False)

    @api.depends('order_line', 'component_compute', 'order_line.product_uom_qty')
    def _compute_component(self):
        for order in self:
            # lines_to_delete = []
            # print("lines_to_delete",lines_to_delete)
            # for line in order.order_line:
            #     print("lines_to_delete333",lines_to_delete)
            #     for component in order.component:
            #         print("exceuteeeeeeddddd2222225555552")
            #
            #         if component.bom_order_line not in order.order_line:
            #             print("55555555555555555555555")
            #
            #             component.unlink()
            #             lines_to_delete.append(line.id)
            #
            # if lines_to_delete:
            #     order.order_line.filtered(lambda line: line.id in lines_to_delete).unlink()
            order.component_compute = False
            if order.order_line:
                for line in order.order_line:

                    if not line.edited and str(line.id).isdigit():
                        if line.product_id.bom_ids:
                            for bom in line.product_id.bom_ids[0]:

                                for component in bom.bom_line_ids:
                                    prorata = (line.product_uom_qty * component.product_qty) / (bom.product_qty)

                                    new_component = self.env['sale.order.component'].create({
                                        'order_line_from_parent': line.product_id.id,
                                        'bom_order_line': line.id,
                                        'new_product': component.product_id.id,
                                        'bom_id': bom.id,
                                        'new_quan': prorata,
                                        'new_uom': component.product_uom_id.id,
                                        'new_forecast': component.product_id.virtual_available,
                                        'line_quantity': line.product_uom_qty,
                                        'component_quantity': component.product_qty,
                                        'bom_quantity': bom.product_qty,

                                    })
                                    order.component |= new_component
                                    line.edited = True

                    else:
                        if line.product_uom_qty and line.edited:
                            for component in order.component:

                                new_id = 'NewId_'
                                if new_id in str(line.id):
                                    new_id = str(line.id).split(new_id)

                                if str(component.bom_order_line.id) == new_id[1]:
                                    component.line_quantity = line.product_uom_qty

                                    if component.bom_quantity != 0:
                                        component.new_quan = (line.product_uom_qty * component.component_quantity) / (
                                            component.bom_quantity)

    def action_confirm(self):
        for product in self.order_line:
            bom_lines = []
            operation_ids = []
            for component in self.component:
                if component.order_line_from_parent.id == product.product_id.id:
                    bom_line_vals = {
                        'bom_id': component.bom_id,
                        'product_id': component.new_product.id,
                        'product_qty': component.new_quan,
                        'product_uom_id': component.new_uom.id,
                    }
                    bom_lines.append((0, 0, bom_line_vals))

            if product.product_id.bom_ids:

                for operation in product.product_id.bom_ids[0].operation_ids:
                    new_operation = operation.copy()
                    # new_operation.bom_id = new_bom
                    operation_ids.append(new_operation.id)
                    print("op id -------------------------------------------- ", operation_ids)

            new_bom_vals = {
                'product_id': product.product_id.id,
                'product_tmpl_id': product.product_id.product_tmpl_id.id,
                'product_qty': product.product_uom_qty,
                'bom_line_ids': bom_lines,
                'operation_ids': operation_ids if operation_ids else None,
                # 'operation_ids': [(6, 0, product.product_id.bom_ids[0].operation_ids.ids)] if
                # product.product_id.bom_ids[0].operation_ids else None,
            }
            print("lllllllllllllllllllllll", product.product_id.bom_ids.operation_ids)
            print('new_bom_vals : ', new_bom_vals)
            if bom_lines:
                new_bom = self.env['mrp.bom'].create(new_bom_vals)
                # new_bom.write({'operation_ids': [(6, 0, operation_ids)]})
                for com in self.component:
                    if com.order_line_from_parent.id == product.product_id.id:
                        com.bom_id = new_bom
        res = super(saleorder, self).action_confirm()
        return res

    @api.onchange('component')
    def _onchange_lines(self):
        if self.component:
            for component in self.component:
                if component.edited_component:
                    self.compute_bool = component.edited_component
                    bool = self.compute_bool


class saleorderline(models.Model):
    _inherit = "sale.order.line"

    edited = fields.Boolean(copy=False)

    def unlink(self):
        print('un linkkkkk ')
        component = self.mapped('order_id.component')
        components_to_delete = component.filtered(lambda com: com.bom_order_line.id in self.ids)
        components_to_delete.unlink()
        res = super(saleorderline, self).unlink()
        return res


class mrpbom(models.Model):
    _inherit = "mrp.bom.line"

    bom_order_line = fields.Many2one('sale.order.line')
