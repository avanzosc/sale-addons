# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Product Catalog Delivery Lead",
    "version": "18.0.1.0.0",
    "summary": "Set the sale order line delivery lead time from the catalog",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/sale-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "depends": [
        "sale_product_catalog",
        "sale_stock",
    ],
    "data": [
        "views/product_catalog_views.xml",
    ],
    "installable": True,
    "application": False,
}
