# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Agreements",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "purchase_requisition",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sale_requisition_security.xml",
        "data/sale_requisition_data.xml",
        "views/sale_order_views.xml",
        "views/sale_requisition_views.xml",
        "views/sale_requisition_type_views.xml",
    ],
    "installable": True,
}
