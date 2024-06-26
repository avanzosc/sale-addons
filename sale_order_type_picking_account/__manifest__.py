# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Type Picking Account",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": ["sale_order_type", "sale", "stock", "account"],
    "excludes": [],
    "data": [
        "views/stock_picking_view.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
