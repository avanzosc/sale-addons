# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Spare Serial Number For BoM product",
    "version": "14.0.1.0.0",
    "depends": [
        "sale",
        "stock",
        "mrp",
    ],
    "author":  "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/sale-addons",
    "data": [
        "views/sale_order_views.xml",
        "views/stock_production_lot_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
}
