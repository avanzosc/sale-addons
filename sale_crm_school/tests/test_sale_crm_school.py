# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from .common import TestSaleCrmSchoolCommon
from odoo.tests import common
from odoo.exceptions import Warning


@common.at_install(False)
@common.post_install(True)
class TestSaleCrmSchool(TestSaleCrmSchoolCommon):

    def test_sale_crm_school(self):
        with self.assertRaises(Warning):
            self.lead.create_sale_order_for_student()
        academic_year = self.academic_year_model.create(
            self.next_academic_year_vals)
        with self.assertRaises(Warning):
            self.lead.create_sale_order_for_student()
        self.lead.future_student_ids.write({
            'academic_year_id': academic_year.id,
        })
        res = self.lead.create_sale_order_for_student()
        for future_student in self.lead.future_student_ids:
            self.assertEquals(future_student.sale_order_id.child_id,
                              future_student.child_id)
        sales = self.lead.mapped('future_student_ids.sale_order_id')
        self.assertIn(('id', 'in', sales.ids), res.get('domain'))
