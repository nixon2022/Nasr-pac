# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'ALTANMYA-Nasrpac Reports',
    'version': '1.0',
    'sequence': -200,
    'category': 'ALTANMYA-Nasrpac Reports',
    'depends': ['account','account_reports'],
    'data': [
        'views/partner_ledger_inherit_template.xml',


    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
