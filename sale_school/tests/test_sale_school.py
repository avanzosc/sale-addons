# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleSchoolCommon
from odoo.tests import common
from odoo.exceptions import UserError, ValidationError


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
        self.edu_group2.write({
            "student_ids": [(4, self.sale_order.child_id.id)],
        })
        self.assertIn(self.sale_order.child_id, self.edu_group2.student_ids)
        self.sale_order.action_cancel()
        self.assertNotIn(
            self.sale_order.child_id, self.sale_order.edu_group_id.student_ids)
        self.assertNotIn(self.sale_order.child_id, self.edu_group2.student_ids)

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

    def test_change_group(self):
        new_center = self.edu_partner.copy()
        new_course = self.edu_course.copy(default={"education_code": "NEXT"})
        next_year = self.academic_year._get_next()
        new_sale_order = self.sale_order.copy(default={
            "academic_year_id": next_year.id,
            "school_id": new_center.id,
            "course_id": new_course.id,
            "edu_group_id": False})
        self.assertFalse(new_sale_order.edu_group_id)
        self.assertEquals(self.sale_order.edu_group_id, self.group)
        sale_orders = self.sale_order | new_sale_order
        with self.assertRaises(UserError):
            self.group_change_model.with_context(
                active_model="sale.order",
                active_ids=sale_orders.ids).create({})
        new_sale_order.academic_year_id = self.sale_order.academic_year_id
        with self.assertRaises(UserError):
            self.group_change_model.with_context(
                active_model="sale.order",
                active_ids=sale_orders.ids).create({})
        new_sale_order.school_id = self.sale_order.school_id
        with self.assertRaises(UserError):
            self.group_change_model.with_context(
                active_model="sale.order",
                active_ids=sale_orders.ids).create({})
        new_sale_order.course_id = self.sale_order.course_id
        new_wizard = self.group_change_model.with_context(
            active_model="sale.order",
            active_ids=sale_orders.ids).create({})
        self.assertEquals(new_wizard.center_id, self.edu_partner)
        self.assertEquals(new_wizard.course_id, self.edu_course)
        new_wizard.group_id = self.group
        new_wizard.button_change_group()
        self.assertEquals(new_sale_order.edu_group_id, self.group)
        new_sale_order.action_confirm()
        self.assertNotIn(new_sale_order.state, ["draft", "sent"])
        with self.assertRaises(UserError):
            self.group_change_model.with_context(
                active_model="sale.order",
                active_ids=new_sale_order.ids).create({})

    def test_create_next_sale_order(self):
        next_course = self.edu_course.copy(default={"education_code": "NEXT"})
        next_year = self.academic_year._get_next()
        next_template = self.sale_template.copy(
            default={"course_id": next_course.id,
                     "school_id": self.edu_partner.id})
        self.env["education.course.change"].create({
            "school_id": self.edu_partner.id,
            "course_id": self.edu_course.id,
            "next_school_id": self.edu_partner.id,
            "next_course_id": next_course.id,
        })
        self.assertFalse(self.student.enrollment_ids.filtered(
            lambda e: e.academic_year_id == next_year))
        wizard = self.enrollment_wizard_model.with_context(
            active_model="res.partner", active_ids=self.student.ids).create({})
        line = wizard.line_ids.filtered(lambda l: l.partner_id == self.student)
        self.assertEquals(line.enroll_action, "pass")
        self.assertEquals(line.next_center_id, self.edu_partner)
        self.assertEquals(line.next_course_id, next_course)
        wizard.button_create_enrollment()
        self.student.create_next_enrollment()
        action_dict = self.student.button_open_enrollments()
        self.assertIn(
            ("child_id", "=", self.student.id), action_dict.get("domain"))
        self.assertIn("default_child_id", action_dict.get("context"))
        self.assertTrue(self.student.enrollment_ids.filtered(
            lambda e: e.academic_year_id == next_year))
        active_enrollments = self.student.enrollment_ids.filtered(
            lambda e: e.state != "cancel")
        self.assertEquals(
            len(active_enrollments), self.student.enrollment_count)
        next_enrollments = self.student.enrollment_ids.filtered(
            lambda e: e.academic_year_id == next_year)
        self.assertEquals(
            next_enrollments[:1].sale_order_template_id, next_template)
        self.student.create_next_enrollment()
        next_enrollments = self.student.enrollment_ids.filtered(
            lambda e: e.academic_year_id == next_year)
        self.assertEquals(len(next_enrollments), 1)
        next_enrollments[:1].action_cancel()
        self.student.create_next_enrollment()
        next_enrollments = self.student.enrollment_ids.filtered(
            lambda e: e.academic_year_id == next_year)
        self.assertEquals(len(next_enrollments), 2)

    def test_student_discontinue(self):
        self.assertFalse(self.student.old_student)
        self.assertEquals(self.student.educational_category, "student")
        wizard = self.enrollment_wizard_model.with_context(
            active_model="res.partner", active_ids=self.student.ids).create({})
        next_year = self.academic_year._get_next()
        self.assertEquals(wizard.academic_year_id, next_year)
        line = wizard.line_ids.filtered(lambda l: l.partner_id == self.student)
        line.enroll_action = "unenroll"
        wizard.button_create_enrollment()
        self.student.create_next_enrollment()
        self.assertTrue(self.student.old_student)
        self.assertEquals(self.student.educational_category, "otherrelative")

    def test_student_repeater_enrollment(self):
        next_year = self.academic_year._get_next()
        current_group = self.student.get_current_group()
        sale_orders = self.sale_order.search([
            ("child_id", "=", self.student.id),
            ("school_id", "=", current_group.center_id.id),
            ("course_id", "=", current_group.course_id.id),
            ("academic_year_id", "=", next_year.id),
        ])
        self.assertFalse(sale_orders)
        self.student.write({
            "enrollment_history_ids": [(0, 0, {
                "academic_year_id": next_year.id,
                "enrollment_action": "repeat",
                "enrollment_center_id": self.student.current_center_id.id,
                "enrollment_course_id": self.student.current_course_id.id,
            })]
        })
        self.student.create_next_enrollment()
        sale_orders = self.sale_order.search([
            ("child_id", "=", self.student.id),
            ("school_id", "=", current_group.center_id.id),
            ("course_id", "=", current_group.course_id.id),
            ("academic_year_id", "=", next_year.id),
        ])
        self.assertTrue(sale_orders)

    def test_create_enroll_history(self):
        students = self.partner_model.search([
            ("educational_category", "=", "student"),
        ])
        next_year = self.academic_year._get_next()
        enrollments = self.enrollment_model.search([
            ("academic_year_id", "=", next_year.id),
        ])
        self.assertFalse(enrollments)
        action_dict = self.partner_model._create_enrollment_history()
        enrollments = self.enrollment_model.search([
            ("academic_year_id", "=", next_year.id),
        ])
        self.assertTrue(enrollments)
        self.assertEquals(len(students), len(enrollments))
        self.assertIn(("academic_year_id", "=", next_year.id),
                      action_dict.get("domain"))
