# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Template Space",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://www.avanzosc.es",
    "depends": [
        "sale_management",
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_template_space_views.xml",
        "views/sale_order_template_views.xml",
        "views/sale_order_template_line_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
