# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Rental",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "stock",
    ],
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Sales",
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/account_invoice_view.xml",
    ],
    "installable": True,
}
