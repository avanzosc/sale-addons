# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Picking Returnable Stock Import",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_stock",
        "base_import_wizard",
        "sale_order_type",
        "sale_picking_return_containers",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/returnable_stock_import_wizard_security.xml",
        "views/returnable_stock_import_view.xml",
        "views/returnable_stock_import_line_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
