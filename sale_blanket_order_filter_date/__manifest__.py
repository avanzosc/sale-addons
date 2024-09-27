# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale blanket Order Filter Date",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": ["sale_blanket_order", "sale_order_line_date"],
    "data": [
        "views/sale_blanket_order_views.xml",
        "wizard/create_sale_order_views.xml",
    ],
    "installable": True,
}
