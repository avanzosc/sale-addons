# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contacts_school_education.tests.common import \
    TestContactsSchoolEducationCommon


class TestSaleSchoolCommon(TestContactsSchoolEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleSchoolCommon, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.enrollment_model = cls.env["res.partner.enrollment"]
        cls.enrollment_wizard_model = cls.env["education.enrollment"]
        cls.group_change_model = cls.env["sale.order.group.change"]
        cls.sale_order_model = cls.env["sale.order"]
        cls.product_model = cls.env["product.product"]
        cls.family_obj = cls.env["res.partner.family"]
        cls.pricelist_obj = cls.env["product.pricelist"]
        cls.edu_partner.educational_category = "school"
        cls.pricelist_type = cls.env["product.pricelist.type"].create({
            "name": "Student Pricelist",
        })
        cls.family_pricelist = cls.pricelist_obj.create({
            "name": "Family Pricelist",
        })
        cls.student_pricelist = cls.pricelist_obj.create({
            "name": "Student Pricelist",
            "type_id": cls.pricelist_type.id,
        })
        cls.student_pricelist2 = cls.student_pricelist.copy(
            default={"child_num": 2})
        cls.family.property_product_pricelist = cls.family_pricelist
        cls.student.property_product_pricelist = cls.student_pricelist
        cls.group.write({
            "student_ids": [(6, 0, cls.student.ids)],
        })
        cls.payment_method = cls.env["account.payment.method"].search([
            ("bank_account_required", "=", True),
        ])
        if not cls.payment_method:
            cls.payment_method = cls.payment_method.create({
                "name": "Test Payment Method",
                "code": "TEST",
                "payment_type": "inbound",
                "bank_account_required": True,
            })
        cls.payment_mode = cls.env["account.payment.mode"].search([
            ("payment_method_id", "=", cls.payment_method.id),
        ])
        if not cls.payment_mode:
            cls.payment_mode = cls.payment_mode.create({
                "name": "Test Payment Mode",
                "payment_method_id": cls.payment_method.id,
                "bank_account_link": "variable",
                "default_journal_ids": cls.env["account.journal"].search([
                    ("type", "in", ("sale", "sale_refund"))])
            })
        progenitor_vals = {
            "name": "Progenitor",
            "educational_category": "progenitor",
            "bank_ids": [(0, 0, {
                "acc_number": "ES2020189263751078650575",
            })],
            "customer_payment_mode_id": False,
        }
        cls.progenitor = cls.partner_model.create(progenitor_vals)
        family_vals = {
            "child2_id": cls.student.id,
            "responsible_id": cls.progenitor.id,
            "family_id": cls.family.id,
            "payer": True,
            "payment_percentage": 100.0,
            "bank_id": cls.progenitor.bank_ids[:1].id,
        }
        cls.family_obj.create(family_vals)
        cls.service = cls.product_model.create({
            "name": "Test Service",
        })
        cls.service2 = cls.service.copy()
        cls.class_type = cls.env['education.group_type'].create({
            'education_code': 'TYPE',
            'description': 'Test Group Type',
            'type': 'class',
        })
        cls.edu_group2 = cls.group.copy(default={
            "education_code": "TEST2",
            "description": "Test Education Group (2)",
            "academic_year_id": cls.group.academic_year_id.id,
            "center_id": cls.edu_partner.id,
            "course_id": cls.edu_course.id,
            "group_type_id": cls.class_type.id,
        })
        cls.sale_order = cls.sale_order_model.create({
            "partner_id": cls.family.id,
            "child_id": cls.student.id,
            "school_id": cls.edu_partner.id,
            "course_id": cls.edu_course.id,
            "academic_year_id": cls.academic_year.id,
            "edu_group_id": cls.group.id,
            "order_line": [(0, 0, {
                "product_id": cls.service.id,
                "payer_ids": [(0, 0, {
                    "payer_id": cls.progenitor.id,
                    "pay_percentage": 50.0,
                })],
            })],
        })
        cls.sale_template = cls.env["sale.order.template"].create({
            "name": "Test Template",
            "course_id": cls.edu_course.id,
            "school_id": cls.edu_partner.id,
            "sale_order_template_line_ids": [(0, 0, {
                "product_id": cls.service.id,
                "name": cls.service.name,
                "price_unit": cls.service.lst_price,
                "product_uom_qty": 10.0,
                "product_uom_id": cls.service.uom_id.id,
            })],
            "sale_order_template_option_ids": [(0, 0, {
                "product_id": cls.service2.id,
                "name": cls.service2.name,
                "price_unit": cls.service2.lst_price,
                "quantity": 10.0,
                "uom_id": cls.service2.uom_id.id,
            })]
        })
