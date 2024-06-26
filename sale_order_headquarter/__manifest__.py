# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Headquarter",
    "version": "14.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "res_partner_headquarter",
        "sale",
    ],
    "data": [
        "security/sale_order_headquarter_security.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
