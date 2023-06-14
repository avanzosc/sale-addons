# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Report Product Attributes",
    'version': '12.0.1.0.0',
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "category": "Sale",
    "depends": [
        "sale",
        "product",
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_report_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
