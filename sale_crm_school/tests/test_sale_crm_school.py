# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from .common import TestSaleCrmSchoolCommon
from odoo.tests import common
from odoo.exceptions import UserError


@common.at_install(False)
@common.post_install(True)
class TestSaleCrmSchool(TestSaleCrmSchoolCommon):

    def test_sale_crm_school(self):
        with self.assertRaises(UserError):
            self.lead.create_sale_order_for_student()
        self.assertTrue(self.next_year)
        with self.assertRaises(UserError):
            self.lead.create_sale_order_for_student()
        self.lead.future_student_ids.write({
            'academic_year_id': self.next_year.id,
        })
        res = self.lead.create_sale_order_for_student()
        for future_student in self.lead.future_student_ids:
            self.assertEquals(future_student.sale_order_id.child_id,
                              future_student.child_id)
        sales = self.lead.mapped('future_student_ids.sale_order_id')
        self.assertIn(('id', 'in', sales.ids), res.get('domain'))

    def test_education_course_change(self):
        search_cond = [
            ("child_id", "=", self.student.id),
            ("school_id", "=", self.edu_partner2.id),
            ("course_id", "=", self.edu_course2.id),
            ("academic_year_id", "=", self.next_year.id),
        ]
        sale_orders = self.sale_order_model.search(search_cond)
        new_students = self.new_student_model.search(search_cond)
        self.assertFalse(sale_orders)
        self.assertFalse(new_students)
        self.student.write({
            "enrollment_history_ids": [(0, 0, {
                "enrollment_action": "pass",
                "academic_year_id": self.next_year.id,
                "enrollment_center_id": self.edu_partner2.id,
                "enrollment_course_id": self.edu_course2.id,
            })],
        })
        self.student.create_next_enrollment()
        sale_orders = self.sale_order_model.search(search_cond)
        new_students = self.new_student_model.search(search_cond)
        self.assertFalse(sale_orders)
        self.assertTrue(new_students)
