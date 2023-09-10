# -*- coding: utf-8 -*-

{
    'name': 'Maintenance',
    'version': '1.0',
    'sequence': 100,
    'category': 'Manufacturing/Maintenance',
    'description': """
        Track equipments and maintenance requests""",
    'depends': ['mail',
                'maintenance',
                'mrp_maintenance',
                'mrp'],
    'summary': 'Track equipment and manage maintenance requests',
    'website': 'https://www.odoo.com/app/maintenance',
    'data': [
            'views/maintenance_request.xml' ],
    # 'demo': ['data/maintenance_demo.xml'],
    # 'installable': True,
    # 'application': True,
    # 'assets': {
    #     'web.assets_backend': [
    #         'maintenance/static/src/**/*',
    #     ],
    # },
    'license': 'LGPL-3',
}
