# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Package Usability",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "website": "http://www.avanzosc.es",
    "category": "Sale",
    "depends": [
        "sale_stock",
        "stock_move_line_force_done"
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_move_line_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
