# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Line Attachment",
    "version": "12.0.1.1.0",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "mail"
    ],
    "category": "Sales",
    "data": [
        "wizard/wiz_catch_attachment_from_product_view.xml",
        "views/sale_order_views.xml",
        "views/ir_attachment_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
