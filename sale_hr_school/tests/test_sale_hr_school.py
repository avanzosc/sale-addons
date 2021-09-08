# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleHrSchoolCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleHrSchool(TestSaleHrSchoolCommon):

    def test_sale_hr_school(self):
        domain = [
            ("school_year_id", "=", self.sale_order.academic_year_id.id),
            ("student_id", "=", self.sale_order.child_id.id),
        ]
        supervised_year = self.supervised_model.search(domain)
        self.assertFalse(supervised_year)
        self.sale_order.write({
            "teacher_id": self.teacher.id,
        })
        self.sale_order.action_confirm()
        supervised_year = self.supervised_model.search(domain)
        self.assertTrue(supervised_year)
        self.sale_order.action_cancel()
        supervised_year = self.supervised_model.search(domain)
        self.assertFalse(supervised_year)

    def test_sale_hr_school_error(self):
        self.assertFalse(self.sale_order.teacher_id)
        self.supervised_model.create({
            "school_year_id": self.sale_order.academic_year_id.id,
            "student_id": self.sale_order.child_id.id,
            "teacher_id": self.teacher.id
        })
        self.sale_order.get_supervising_teacher()
        self.assertEquals(self.sale_order.teacher_id, self.teacher)
