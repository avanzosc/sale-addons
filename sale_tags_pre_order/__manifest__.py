# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Tags Pre-Order",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sales_team",
        "shopify_ept",
    ],
    "excludes": [],
    "data": [
        "views/crm_tag_view.xml",
        "views/shopify_payment_gateway_ept_view.xml",
    ],
    "installable": True,
}
