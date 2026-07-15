# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Final Customer Address",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": """Adds a final customer flag on delivery addresses and
    filters sale order shipping addresses""",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale_required_shipping_address",
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
