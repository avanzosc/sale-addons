# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Emptying Location",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_order_type_picking",
        "sale_order_lot_selection",
        "stock_picking_emptying_location",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
