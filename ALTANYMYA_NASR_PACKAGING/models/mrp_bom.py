from odoo import fields, models


class MrpBomNasr(models.Model):
    _inherit = 'mrp.bom'
    remarks = fields.Html(string="Remarks")


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'
    mr = fields.Boolean(string="MR")
