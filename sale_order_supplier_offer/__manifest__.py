# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Supplier Offer",
    "version": "14.0.1.0.0",
    "depends": [
        "sale",
        "purchase",
        "purchase_stock"
    ],
    "author":  "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/sale-addons",
    "data": [
        "views/purchase_order_views.xml",
        "views/sale_order_views.xml",
    ],
    "post_init_hook": "purchase_order_with_sale_order",
    "installable": True,
}
