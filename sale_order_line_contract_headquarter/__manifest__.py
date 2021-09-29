# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Sale Order Line Contract Headquarter',
    'version': '14.0.1.0.0',
    'depends': [
        'sale_order_line_contract',
        'account_headquarter',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'website': 'http://www.avanzosc.es',
    'data': [
        'security/sale_order_line_contract_headquarter_security.xml',
        'views/contract_contract_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}
