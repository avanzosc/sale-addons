# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Import Wizard",
    "version": "16.0.1.0.0",
    "category": "Hidden/Tools",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
        "sales_team",
        "base_import_wizard",
        "product_trim_name",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_import_wizard_security.xml",
        "views/sale_order_import_line_views.xml",
        "views/sale_order_import_views.xml",
        "views/sale_order_views.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
}
