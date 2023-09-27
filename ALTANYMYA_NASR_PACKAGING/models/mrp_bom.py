from odoo import fields, models


class MrpBomNasr(models.Model):
    _inherit = 'mrp.bom'
    remarks = fields.Html(string="Remarks")


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'
    mr = fields.Boolean(string="MR", related='operation_id.mr')


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'
    mr = fields.Boolean(string="MR")
