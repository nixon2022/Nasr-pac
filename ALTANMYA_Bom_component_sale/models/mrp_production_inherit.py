from odoo import api, fields, models, tools, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_moves_raw_values(self):
        moves = []
        # for production in self.sale_order_id.component:
        #
        #     print("production",production)
        for production in self:
            print("production ISSS", production)
            print("production bom id ISSS", production.sale_order_id.component)
            print("production bom id ", production.bom_id)

            component = production.sale_order_id.component.mapped('bom_id')

            if component:
                components_filtered = component.filtered(lambda com: com.product_tmpl_id.id == production.product_id.product_tmpl_id.id)
            # print("components_filtered", component , components_filtered)
            if components_filtered:
                production.bom_id = components_filtered
            if not production.bom_id:
                continue
            factor = production.product_uom_id._compute_quantity(production.product_qty,
                                                                 production.bom_id.product_uom_id) / production.bom_id.product_qty

            print("###############################################################",
                  production.bom_id.explode(production.product_id, factor,
                                            picking_type=production.bom_id.picking_type_id))

            boms, lines = production.bom_id.explode(production.product_id, factor,
                                            picking_type=production.bom_id.picking_type_id)
            print("********************", factor)
            print("********************", boms)
            print("********************", lines)
            for bom_line, line_data in lines:
                print("--------bom line ------", bom_line)
                print("--------line_data ------", line_data)

                if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom' or \
                        bom_line.product_id.type not in ['product', 'consu']:
                    continue
                print("operation id >>>>>>>>",bom_line.allowed_operation_ids)
                print("operation id  is>>>>>>>>",bom_line.operation_id)
                # print("operation id  is>>>>>>>>>>>>>>>>>", line_data['parent_line'].operation_id.id)

                operation = bom_line.operation_id.id or line_data['parent_line'] and line_data[
                    'parent_line'].operation_id.id
                print("operations -----------",operation)
                moves.append(production._get_move_raw_values(
                    bom_line.product_id,
                    line_data['qty'],
                    bom_line.product_uom_id,
                    operation,
                    bom_line
                ))
        print("moces is +++++++",moves)
        return moves

    # def _create_workorder(self):
    #     for production in self:
    #         if not production.bom_id or not production.product_id:
    #             continue
    #         workorders_values = []
    #
    #         product_qty = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id)
    #         exploded_boms, dummy = production.bom_id.explode(production.product_id, product_qty / production.bom_id.product_qty, picking_type=production.bom_id.picking_type_id)
    #
    #         for bom, bom_data in exploded_boms:
    #
    #
    #             print("@@@@@@@@@@@@@@@@@@@ bom ", bom)
    #             print("@@@@@@@@@@@@@@@@@@@ bom dataaa  ", bom_data)
    #             print("@@@@@@@@@@@@@@@@@@@ bom dataaa parent line  ", bom_data['parent_line'])
    #             # If the operations of the parent BoM and phantom BoM are the same, don't recreate work orders.
    #             if not (bom.operation_ids and (not bom_data['parent_line'] or bom_data['parent_line'].bom_id.operation_ids != bom.operation_ids)):
    #                 continue
    #             for operation in bom.operation_ids:
    #                 print("OPEEEEEEEEEEEEEEEEE__________________",operation)
    #                 if operation._skip_operation_line(bom_data['product']):
    #                     continue
    #                 workorders_values += [{
    #                     'name': operation.name,
    #                     'production_id': production.id,
    #                     'workcenter_id': operation.workcenter_id.id,
    #                     'product_uom_id': production.product_uom_id.id,
    #                     'operation_id': operation.id,
    #                     'state': 'pending',
    #                 }]
    #         production.workorder_ids = [(5, 0)] + [(0, 0, value) for value in workorders_values]
    #         for workorder in production.workorder_ids:
    #             workorder.duration_expected = workorder._get_duration_expected()

