# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Contract Specification',
    'version': '11.0.1.0.0',
    'category': 'Sale Management',
    'author': 'AvanzOsc',
    'license': 'AGPL-3',
    'summary': 'Define conditions and specifications in sale orders',
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_condition_views.xml',
        'views/sale_condition_template_views.xml',
        'views/sale_order_views.xml',
        'views/sale_contract_specification_menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
