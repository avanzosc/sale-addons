# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Blanket Order Line Customer",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/sale-addons",
    "author": "AvanzOSC",
    "depends": [
        "sale_blanket_order",
    ],
    "data": [
        "views/sale_blanket_order_line_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
