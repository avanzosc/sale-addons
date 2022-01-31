# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Offer Version",
    "version": "14.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author":  "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "sale_order_type",
        "sale_order_revision",
    ],
    "data": [
        "data/sale_order_offer_version.xml",
        "views/sale_order_type_views.xml",
        "views/sale_order_views.xml",
        "reports/sale_order_report_template.xml",
    ],
    "installable": True,
}
