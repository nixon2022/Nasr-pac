from odoo import fields, models


class ResPartnerNasr(models.Model):
    _inherit = 'res.partner'

    arabic_name_nasr = fields.Char(string="اسم العميل")
    company_new_field = fields.Char(string="Company ID")

