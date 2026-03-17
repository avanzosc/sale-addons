# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Import Wizard Type",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/sale-addons",
    "author": "AvanzOSC",
    "summary": "Allows setting sale order type when importing sale orders",
    "depends": [
        "sale_import_wizard",
        "sale_order_type",
    ],
    "data": [
        "views/sale_order_import_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
