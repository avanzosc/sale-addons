# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Commission Invoice Report",
    "version": "14.0.1.2.0",
    "category": "Sales Management",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "account",
        "sale_commission",
    ],
    "excludes": [],
    "data": [
        "data/paperformat.xml",
        "reports/sale_commission_settlement_invoice_report.xml",
        #        "views/account_move_views.xml",
    ],
    "installable": True,
}
