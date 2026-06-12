# Copyright 2026 Alfredo de la fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Old Account Analytic Account",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": ["sale_project"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_put_project_in_sale_orders",
}
