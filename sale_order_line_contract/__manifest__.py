# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Sale Order Line Contract',
    'version': '12.0.1.0.0',
    'depends': [
        'contract',
        'sale',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/product_product_views.xml',
        'views/sale_order_views.xml',
        'views/contract_contract_views.xml',
        'views/contract_line_views.xml',
    ],
    'installable': True,
}
