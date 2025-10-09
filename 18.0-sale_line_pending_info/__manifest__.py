# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# Copyright 2025 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Line Pending Info",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": """Adds pending delivery and invoicing
    information to sale orders and lines""",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
        "sale_stock",
        "sale_order_line_input",
        "sale_order_line_menu",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
        "reports/sale_report.xml",
    ],
    "test": [
        "tests/test_sale_line_pending_info.py",
    ],
    "installable": True,
    "application": False,
}
