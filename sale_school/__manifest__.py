# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales for School",
    "version": "12.0.1.1.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "sale_crm",
        "sale_management",
        "crm_school",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/crm_lead_view.xml",
        "views/crm_lead_future_student_view.xml",
        "views/sale_order_template_view.xml",
        "views/product_category_view.xml",
    ],
    "installable": True,
}
