from odoo import api, fields, models, tools, _


class saleorder(models.Model):
    _inherit = "sale.order"

    component = fields.Many2many('sale.order.component', string='order', copy=False)
    component_compute = fields.Boolean(compute='_compute_component')
    compute_bool=fields.Boolean(string='bool', copy=False)
    my_alert=fields.Boolean(string='bool', copy=False)

    @api.depends('order_line', 'component_compute')
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
            # if order.component_compute:
            print("exceuteeeeeeddddd222")
            if order.order_line:
                for line in order.order_line:
                    print("-------------------", line.edited, str(line.id).isdigit())
                    if not line.edited and str(line.id).isdigit():
                        print("product_id", line.product_id)
                        for bom in line.product_id.bom_ids:
                            print("product_id", line.product_id.bom_ids.product_uom_id)
                            for component in bom.bom_line_ids:
                                new_component = self.env['sale.order.component'].create({
                                    'order_line_from_parent': line.product_id.id,
                                    'bom_order_line': line.id,
                                    'new_product': component.product_id.id,
                                    'bom_id': bom.id,
                                    'new_quan': component.product_qty,
                                    'new_uom': component.product_uom_id.id,
                                })
                                order.component |= new_component
                                line.edited = True

    def action_confirm(self):
        for product in self.order_line:
            print("product", product)
            bom_lines = []
            for component in self.component:
                # print("after confirm ", rec)
                # print("product ", rec.order_line.product_id)
                # print("out 1 ----- ", component)
                # print("bom is  ----- ", component.bom_id)
                if component.order_line_from_parent.id == product.product_id.id:
                    # print("edited", component.edited_component)
                    bom_line_vals = {
                        'bom_id': component.bom_id,
                        'product_id': component.new_product.id,
                        'product_qty': component.new_quan,
                        'product_uom_id': component.new_uom.id,
                    }
                    bom_lines.append((0, 0, bom_line_vals))
                    if component.edited_component:
                        # bool =self.compute_bool=component.edited_component
                        # print("bool" ,bool)

                        rec_id = self.env['ir.model'].sudo().search([('model', '=', 'sale.order')],
                                                                    limit=1)

                        self.env['mail.activity'].sudo().create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
                            # 'date_deadline': date.today(),
                            'summary': '%s component have been changed' % (component.new_product.name),
                            'user_id': self.env.user.id,
                            'res_model_id': rec_id.id,
                            'res_id': self.id
                        })

            # print("out ", rec.order_line.product_id)
            # print("out 2 ----- ", component.new_product.id)
            # print("out 3 ----- ", component.new_quan)
            # print("out 4 ----- ", rec.order_line.product_id.product_variant_id.id)
            # print("out 5 ----- ", rec.order_line.product_id.id)
            # print("out 6 ----- ", rec.order_line.product_id.product_tmpl_id.id)
            new_bom_vals = {
                'product_id': product.product_id.id,
                'product_tmpl_id': product.product_id.product_tmpl_id.id,
                'product_qty': product.product_uom_qty,
                'bom_line_ids': bom_lines,
            }
            # print("bom lines", bom_lines)
            if bom_lines:
                new_bom = self.env['mrp.bom'].create(new_bom_vals)
                for com in self.component:
                    if com.order_line_from_parent.id == product.product_id.id:
                        com.bom_id = new_bom
                        print("----commmmmmmmm---------------", com.bom_id)
        res = super(saleorder, self).action_confirm()
        print("res", res)
        return res

    @api.onchange('component')
    def _onchange_lines(self):
        if self.component:
            for component in self.component:
                if component.edited_component:
                    self.compute_bool = component.edited_component
                    bool =self.compute_bool
                    print("bool", bool)






class saleorderline(models.Model):
    _inherit = "sale.order.line"

    edited = fields.Boolean(copy=False)

    def unlink(self):
        print('un linkkkkk ')
        component = self.mapped('order_id.component')
        components_to_delete = component.filtered(lambda com: com.bom_order_line.id in self.ids)
        components_to_delete.unlink()
        # for com in component:
        #     if com.bom_order_line.id == self.id:
        #         print('un-----------link ', com.new_product)
        #         com.unlink()
        res = super(saleorderline, self).unlink()
        return res


class mrpbom(models.Model):
    _inherit = "mrp.bom.line"

    bom_order_line = fields.Many2one('sale.order.line')


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
            res = {'warning': {
                'title': _('Warning'),
                'message': _('My warning message.')
            }}
        if res:
            return res
# mail_activity_data_warning