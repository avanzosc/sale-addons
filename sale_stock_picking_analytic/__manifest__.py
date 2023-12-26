# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales and Warehouse Management - Analytic",
    "summary": "Glue module between sale_stock and stock_picking_analytic",
    "version": "16.0.1.0.0",
    "category": "Hidden",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_stock",
        "stock_picking_analytic",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
