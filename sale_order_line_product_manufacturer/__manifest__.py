{
    "name": "Sale Order Line -  Manufacturer",
    "version": "14.0.1.0.0",
    "summary": "Adds manufacturer field "
    "to invoice and sale order lines pivot views.",
    "category": "Accounting",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "product_manufacturer",
        "mrp_sale_info",
    ],
    "data": [
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
}
