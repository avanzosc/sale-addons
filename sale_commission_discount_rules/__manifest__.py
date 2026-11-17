# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Commission Discount Rules",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/sale-addons",
    "category": "Commission",
    "version": "18.0.0.1.0",
    "license": "AGPL-3",
    "depends": [
        "sale_commission_oca",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/commission_view.xml",
    ],
    "installable": True,
    "application": False,
}
