# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Confirm Usability",
    'version': '16.0.1.0.0',
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "account",
        "sale",
        "sale_stock",
        "stock_move_line_force_done",
        "sale_order_lot_selection",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
    ],
    'installable': True,
}
