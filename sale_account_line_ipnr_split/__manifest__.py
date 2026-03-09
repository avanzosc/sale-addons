# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Account Line IPNR Split",
    "summary": "Breakdown of IPNR into separate lines on invoices and sales orders",
    "version": "16.0.1.0.0",
    "category": "Accounting/Invoicing",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
        "account",
        "l10n_es_aeat_mod592",
    ],
    "data": [
        "views/account_move_views.xml",
        "views/sale_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
