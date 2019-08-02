# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Sales Team Analytic Tag',
    'version': '12.0.1.1.0',
    'depends': [
        'sale',
        'sales_team',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Sales Team Analytic Tag''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'view/crm_team_view.xml',
    ],
    'installable': True,
}
