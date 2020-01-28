# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.addons.sale_school.tests.common import TestSaleSchoolCommon
from odoo import fields


class TestSaleCrmSchoolCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleCrmSchoolCommon, cls).setUpClass()
        cls.lead_model = cls.env['crm.lead']
        cls.service.write({
            'company_id': cls.env.user.company_id.id,
        })
        today = fields.Date.today()
        date_from = today.replace(month=1, day=1)
        date_to = today.replace(year=today.year + 1, month=12, day=31)
        cls.next_academic_year_vals = {
            'name': 'NEXT_YEAR'.format(date_to.year, date_from.year),
            'date_start': date_from,
            'date_end': date_to,
        }
        future_student_vals = {
            'name': 'Student for test sale_crm_school',
            'child_id': cls.student.id,
            'birth_date': '2015-01-01',
            'gender': 'male',
            'school_id': cls.edu_partner.id,
            'course_id': cls.edu_course.id,
        }
        lead_vals = {
            'name': 'Lead for test sale_crm_school',
            'partner_id': cls.family.id,
            'future_student_ids': [(0, 0, future_student_vals)]}
        cls.lead = cls.lead_model.create(lead_vals)
