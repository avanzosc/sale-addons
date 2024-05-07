# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Stock Move Cost",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "stock_move_cost",
        "sale_stock",
    ],
    "excludes": [],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
