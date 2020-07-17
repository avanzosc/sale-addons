# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Analytic',
    'version': '12.0.2.0.0',
    'depends': [
        'analytic',
        'analytic_usability',
        'sale',
    ],
    'author':  "AvanzOSC",
    'license': "AGPL-3",
    'summary': '''Sale Analytic''',
    'website': 'http://www.avanzosc.es',
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
