# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order From Picking',
    'version': '12.0.2.0.0',
    'depends': [
        'sale',
        'stock',
        'sale_stock',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Sale Order From Picking''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'wizard/generate_sale_orders_view.xml',
        ],
    'installable': True,
    'auto_install': False,
}
