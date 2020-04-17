# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleSchoolCommon
from odoo.tests import common
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestSaleSchool(TestSaleSchoolCommon):

    def test_payer_name(self):
        payer = self.sale_order.mapped('order_line.payer_ids')[:1]
        self.assertEquals(
            payer.display_name,
            "{} ({} %)".format(payer.payer_id.name, payer.pay_percentage))

    def test_sale_school(self):
        sale_line = self.sale_order.order_line[:1]
        self.assertEquals(
            sale_line.total_percentage,
            sum(sale_line.mapped('payer_ids.pay_percentage')))
        with self.assertRaises(ValidationError):
            self.sale_order.action_confirm()
        self.assertEquals(len(sale_line.payer_ids), 1)
        payer_line = sale_line.payer_ids[:1]
        self.assertTrue(payer_line.allowed_payers_ids)
        self.assertEquals(payer_line.child_id, self.sale_order.child_id)
        self.assertIn(payer_line.payer_id, payer_line.allowed_payers_ids)
        payer_line.write({
            'pay_percentage': 100.0,
        })
        with self.assertRaises(ValidationError):
            self.sale_order.action_confirm()
        payer_line._onchange_payer_id()
        self.sale_order.action_confirm()
        self.assertIn(
            self.sale_order.child_id, self.sale_order.edu_group_id.student_ids)
        self.sale_order.action_cancel()
        self.assertNotIn(
            self.sale_order.child_id, self.sale_order.edu_group_id.student_ids)

    def test_sale_order_onchange(self):
        self.student.property_product_pricelist = self.student_pricelist
        self.assertNotEquals(
            self.student_pricelist, self.family_pricelist)
        self.assertNotEquals(
            self.student.property_product_pricelist,
            self.family.property_product_pricelist)
        self.assertEquals(
            self.sale_order.pricelist_id,
            self.sale_order.partner_id.property_product_pricelist)
        self.assertFalse(self.sale_order.sale_order_template_id)
        self.sale_order.onchange_school_course()
        self.assertEquals(
            self.sale_order.sale_order_template_id, self.sale_template)
        self.sale_order.onchange_partner_id()
        self.assertEquals(
            self.sale_order.pricelist_id, self.student_pricelist)
        self.assertNotEquals(
            self.sale_order.pricelist_id, self.family_pricelist)

    def test_sale_template(self):
        self.assertEquals(self.edu_course.sale_order_template_count, 1)
        action_dict = self.edu_course.button_open_sale_order_templates()
        self.assertIn(
            ("course_id", "=", self.edu_course.id), action_dict.get("domain"))

    def test_sale_order_no_partner(self):
        sale_order = self.sale_order.copy(default={'partner_id': False})
        self.assertEquals(sale_order.partner_id, sale_order.child_id.parent_id)

    def test_course_change_template(self):
        changes = course_change_obj = self.env["education.course.change"]
        templates = tmpl_obj = self.env["sale.order.template"]
        next_course = self.edu_course.copy(default={"education_code": "NEXT"})
        self.assertEquals(next_course.sale_order_template_count, 0)
        self.assertEquals(self.edu_course.sale_order_template_count, 1)
        changes |= course_change_obj.create({
            "school_id": self.edu_partner.id,
            "course_id": self.edu_course.id,
            "next_school_id": self.edu_partner.id,
            "next_course_id": next_course.id,
        })
        self.assertEquals(self.edu_course.sale_order_template_count, 1)
        templates |= tmpl_obj.search([
            ("school_id", "=", self.edu_partner.id),
            ("course_id", "=", self.edu_course.id),
        ])
        changes |= course_change_obj.create({
            "school_id": self.edu_partner.id,
            "course_id": next_course.id,
            "next_school_id": self.edu_partner.id,
            "next_course_id": self.edu_course.id,
        })
        action_dict = changes.create_sale_order_template()
        templates |= tmpl_obj.search([
            ("school_id", "=", self.edu_partner.id),
            ("course_id", "=", next_course.id),
        ])
        self.assertEquals(next_course.sale_order_template_count, 1)
        self.assertEquals(len(templates), 2)
        self.assertIn(("id", "in", templates.ids), action_dict.get("domain"))
