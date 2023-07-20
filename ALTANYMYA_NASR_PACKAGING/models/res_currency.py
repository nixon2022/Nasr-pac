from odoo import models, fields


class ResCurrencyNasr(models.Model):
    _inherit = 'res.currency'

    unit_arabic = fields.Char(string="Currency Unit in Arabic")
    subunit_arabic = fields.Char(string="Currency Subunit in Arabic")
