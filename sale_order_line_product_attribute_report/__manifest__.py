# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Line Product Attribute Report",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
        "product_attribute_value_image"
    ],
    "data": [
        "data/layouts.xml",
        "data/sale_order_line_product_attribute_report.xml",
        "reports/sale_order_line_product_attribute_report.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
