# -*- coding: utf-8 -*-
###################################################################################
#
#    ALTANMYA - TECHNOLOGY SOLUTIONS
#    Copyright (C) 2022-TODAY ALTANMYA - TECHNOLOGY SOLUTIONS Part of ALTANMYA GROUP.
#    ALTANMYA - Syrian Invoice Module.
#    Author: ALTANMYA for Technology(<https://tech.altanmya.net>)
#
#    This program is Licensed software: you can not modify
#   #
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'ALTANMYA-BoM component ',
    'version': '1.0',
    'sequence': -200,
    'category': 'ALTANMYA-BoM component ',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line_view.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'ALTANMYA_Bom_component_sale/static/src/js/warning_notification.js',
        ],
        'web.report_assets_backend': [
            'ALTANMYA_Bom_component_sale/static/src/js/warning_notification.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
