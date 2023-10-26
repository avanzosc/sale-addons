# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Billing Type",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "sales_team"
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_billing_type_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
