# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.education.tests.common import TestEducationCommon


class TestSaleSchoolCommon(TestEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleSchoolCommon, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.sale_order_model = cls.env["sale.order"]
        cls.product_model = cls.env["product.product"]
        cls.family_obj = cls.env["res.partner.family"]
        cls.pricelist_obj = cls.env["product.pricelist"]
        cls.edu_partner.educational_category = "school"
        cls.family_pricelist = cls.pricelist_obj.create({
            "name": "Family Pricelist",
        })
        cls.student_pricelist = cls.pricelist_obj.create({
            "name": "Student Pricelist",
        })
        family_vals = {
            "name": "Family for test sale_school_generate_sepa",
            "educational_category": "family",
            "property_product_pricelist": cls.family_pricelist.id,
        }
        cls.family = cls.partner_model.create(family_vals)
        student_vals = {
            "name": "Student for test sale_school_generate_sepa",
            "educational_category": "student",
            "parent_id": cls.family.id,
        }
        cls.student = cls.partner_model.create(student_vals)
        progenitor_vals = {
            "name": "Progenitor for test sale_school_generate_sepa",
            "educational_category": "progenitor",
            "bank_ids": [(0, 0, {
                "acc_number": "ES2020189263751078650575",
            })],
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
        cls.sale_order = cls.sale_order_model.create({
            "partner_id": cls.family.id,
            "child_id": cls.student.id,
            "school_id": cls.edu_partner.id,
            "course_id": cls.edu_course.id,
            "academic_year_id": cls.academic_year.id,
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
            })]
        })
