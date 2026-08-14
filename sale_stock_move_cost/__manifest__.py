# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Stock Move Cost",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "stock_move_cost",
        "sale_stock",
    ],
    "excludes": [],
    "data": [
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    "auto_install": True,
    "pre_init_hook": "_pre_init_sale_stock_move_cost",
    "post_init_hook": "_post_init_sale_stock_move_cost",
}
