from odoo import models, fields


class ResCountryNasr(models.Model):
    _inherit = 'res.country'

    arabic_name = fields.Char('Arabic Country Name')
