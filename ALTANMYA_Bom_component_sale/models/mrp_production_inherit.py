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
            print("components_filtered", component , components_filtered)
            if components_filtered:
                production.bom_id = components_filtered
            if not production.bom_id:
                continue
            factor = production.product_uom_id._compute_quantity(production.product_qty,
                                                                 production.bom_id.product_uom_id) / production.bom_id.product_qty

            # print("###############################################################",
            #       production.bom_id.explode(production.product_id, factor,
            #                                 picking_type=production.bom_id.picking_type_id))

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
                operation = bom_line.operation_id.id or line_data['parent_line'] and line_data[
                    'parent_line'].operation_id.id
                moves.append(production._get_move_raw_values(
                    bom_line.product_id,
                    line_data['qty'],
                    bom_line.product_uom_id,
                    operation,
                    bom_line
                ))
        print("moces is +++++++",moves)
        return moves
