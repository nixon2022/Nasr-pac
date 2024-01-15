{
    "name": "Sale MRP BOM",
    "category": "Sale",
    "license": "AGPL-3",
    'author': 'Mustafa Mustafa',
    'company': 'Al-Tanmya IT Solution',
    'website': "https://www.odoo.com",
    'description': """
    """,
    "summary": "Allows define a BOM in the sales lines.",
    "depends": ["mrp", "sale_stock"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_line.xml",
        "views/mrp_bom.xml",
    ],
    "installable": True,
    'assets': {
        'web.assets_backend': [
            "altanmia_sale_mrp_bom/static/src/js/**/*",
            'altanmia_sale_mrp_bom/static/src/scss/style.scss',
        ]
    },
}
