# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.addons.sale_school.tests.common import TestSaleSchoolCommon
from odoo import fields


class TestSaleCrmSchoolCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleCrmSchoolCommon, cls).setUpClass()
        cls.lead_model = cls.env['crm.lead']
        cls.education_plan_model = cls.env['education.plan']
        cls.education_level_model = cls.env['education.level']
        cls.education_course_model = cls.env['education.course']
        cls.academic_year_model = cls.env['education.academic_year']
        cls.sale_template_model = cls.env['sale.order.template']
        education_plan_vals = {
            'description': 'Education plan for test sale_crm_school',
            'education_code': 'PLAN'}
        cls.education_plan = cls.education_plan_model.create(
            education_plan_vals)
        education_level_vals = {
            'education_code': 'LVL1',
            'description': 'Level for test sale_crm_school',
            'short_description': 'L-1',
            'plan_id': cls.education_plan.id}
        cls.education_level = cls.education_level_model.create(
            education_level_vals)
        education_course_vals = {
            'education_code': 'CRS1',
            'level_id': cls.education_level.id,
            'description': 'Course 1'}
        cls.education_course = cls.education_course_model.create(
            education_course_vals)
        cls.service.write({
            'company_id': cls.env.user.company_id.id,
        })
        cls.sale_template = cls.sale_template_model.create({
            'name': 'Test Template',
            'course_id': cls.education_course.id,
            'school_id': cls.edu_partner.id,
            'sale_order_template_line_ids': [(0, 0, {
                'product_id': cls.service.id,
                'name': cls.service.name,
                'price_unit': cls.service.lst_price,
                'product_uom_qty': 10.0,
                'product_uom_id': cls.service.uom_id.id,
            })]
        })
        today = fields.Date.today()
        date_from = today.replace(month=1, day=1)
        date_to = today.replace(year=today.year + 1, month=12, day=31)
        cls.academic_year_vals = {
            'name': '{}+{}'.format(date_to.year, date_from.year),
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
