# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Line Client Order Ref Tree View",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_order_line_menu",
    ],
    "data": [
        "views/sale_order_line_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_client_ref_in_lines",
}
