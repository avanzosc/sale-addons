# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Sintra",
    "version": "18.0.1.0.0",
    "summary": "Sintra objectives grouping sale orders",
    "category": "Sales/Sales",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "purchase",
        "sale",
    ],
    "data": [
        "security/sale_sintra_groups.xml",
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "views/sale_sintra_views.xml",
        "views/sale_order_views.xml",
        "wizards/sale_sintra_assign_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
