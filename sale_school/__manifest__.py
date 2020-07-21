# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales for School",
    "version": "12.0.3.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale",
        "sale_management",
        "sales_team",
        "contacts_school",
        "contacts_school_education",
        "education",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/education_course_view.xml",
        "views/education_course_change_view.xml",
        "views/product_view.xml",
        "views/res_partner_view.xml",
        "views/res_partner_enrollment_view.xml",
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
        "views/sale_order_line_payer_view.xml",
        "views/sale_order_template_view.xml",
        "wizards/education_enrollment_view.xml",
        "wizards/sale_order_group_change_view.xml",
    ],
    "installable": True,
}
