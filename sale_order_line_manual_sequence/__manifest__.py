# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Line Manual Sequence",
    "version": "13.0.1.1.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "stock",
        "account"
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
}
