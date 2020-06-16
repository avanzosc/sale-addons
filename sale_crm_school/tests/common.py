# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.addons.sale_school.tests.common import TestSaleSchoolCommon


class TestSaleCrmSchoolCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleCrmSchoolCommon, cls).setUpClass()
        cls.lead_model = cls.env['crm.lead']
        cls.new_student_model = cls.env["crm.lead.future.student"]
        cls.service.write({
            'company_id': cls.env.user.company_id.id,
        })
        cls.next_year = cls.academic_year._get_next()
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
        cls.course_change = cls.change_model.create({
            'school_id': cls.edu_partner.id,
            'next_school_id': cls.edu_partner2.id,
            'course_id': cls.edu_course.id,
            'next_course_id': cls.edu_course2.id,
        })
