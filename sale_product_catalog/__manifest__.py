# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Product Catalog",
    "version": "18.0.1.1.0",
    "summary": "Product catalog management for sales",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "product",
        "product_pricelist_item_menu",
        "sale",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/product_catalog_rules.xml",
        "data/product_catalog_type_data.xml",
        "views/product_catalog_type_views.xml",
        "views/product_catalog_views.xml",
        "views/product_pricelist_item_views.xml",
        "views/sale_order_views.xml",
        "views/menus.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
