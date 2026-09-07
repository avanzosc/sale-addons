# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Invoice Terms Conditions",
    "version": "18.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/sale-addons",
    "category": "Sales/Sales",
    "depends": ["sale", "sales_team", "account"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "post_init_hook": "_post_install_sale_order_invoice_terms_conditions",
}
