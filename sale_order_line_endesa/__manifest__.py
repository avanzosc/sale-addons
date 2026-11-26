# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Line Endesa",
    "version": "18.0.1.0.0",
    "summary": "Endesa delivery tracking on sale order lines",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "sale_mrp",
        "web_tree_dynamic_colored_field",
    ],
    "data": [
        "security/sale_order_line_endesa_groups.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "views/menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_order_line_endesa/static/src/fields/*",
        ],
    },
    "installable": True,
    "application": False,
}
