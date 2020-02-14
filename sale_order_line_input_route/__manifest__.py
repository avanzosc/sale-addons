# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Line Input - Show routes",
    "summary": "Warning: this module installs purchase and mrp",
    "version": "12.0.1.0.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_order_line_input",
        "stock",
        "purchase_stock",
        "mrp",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
    ],
    "installable": True,
}
