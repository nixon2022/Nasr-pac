from odoo import models, fields


class ResCompanyNasr(models.Model):
    _inherit = 'res.company'

    arabic_name = fields.Char('Name')
    fax = fields.Char(string="Fax")
