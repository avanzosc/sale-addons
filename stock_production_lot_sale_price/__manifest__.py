# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Production Lot Sale Price",
    'version': '14.0.1.0.0',
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock",
        "sale",
        "stock_move_line_cost",
    ],
    "data": [
        "views/stock_production_lot_view.xml",
    ],
    'installable': True,
}
