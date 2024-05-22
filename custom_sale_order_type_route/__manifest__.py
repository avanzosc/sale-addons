# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Custom Sale Order Type Route",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Sales",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_stock",
        "sale_order_type",
        "sale_order_user_usability",
        "sale_line_pending_info",
        "sale_order_line_qty_by_packaging",
        "custom_saca_intercompany",
        "sale_order_line_containers",
        "stock_picking_date_done",
    ],
    "data": [
        "views/sale_order_type_view.xml",
        "views/sale_order_view.xml",
        "views/account_payment_view.xml",
        "views/account_move_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_picking_type_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
