# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Line Commitment Date",
    "version": "14.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
        "sale_stock",
        "sale_order_line_input",
        "sale_order_type",
        "sale_line_pending_info",
        "sale_order_line_menu",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
    ],
    "installable": True,
}
