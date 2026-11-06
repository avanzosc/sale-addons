# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Line Import Wizard",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "base_import_wizard",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_line_import_line_views.xml",
        "views/sale_order_line_import_views.xml",
        "views/sale_order_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
