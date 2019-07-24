# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import ValidationError


class TestSaleCrmSchool(TransactionCase):

    def setUp(self):
        super(TestSaleCrmSchool, self).setUp()
        self.partner_model = self.env['res.partner']
        self.lead_model = self.env['crm.lead']
        self.education_plan_model = self.env['education.plan']
        self.education_level_model = self.env['education.level']
        self.education_course_model = self.env['education.course']
        self.academic_year_model = self.env['education.academic_year']
        self.sale_template_model = self.env['sale.order.template']
        self.sale_order_model = self.env['sale.order']
        self.family_obj = self.env['res.partner.family']
        school_vals = {
            'name': 'School for test sale_crm_school',
            'educational_category': 'school'}
        self.school = self.partner_model.create(school_vals)
        student_vals = {
            'name': 'Student for test sale_crm_school',
            'educational_category': 'student'}
        self.student = self.partner_model.create(student_vals)
        family_vals = {
            'name': 'Family for test sale_crm_school',
            'educational_category': 'family'}
        self.family = self.partner_model.create(family_vals)
        progenitor_vals = {
            'name': 'Progenitor for test sale_crm_school',
            'educational_category': 'progenitor'}
        self.progenitor = self.partner_model.create(progenitor_vals)
        education_plan_vals = {
            'description': 'Education plan for test sale_crm_school',
            'education_code': 'code-1'}
        self.education_plan = self.education_plan_model.create(
            education_plan_vals)
        education_level_vals = {
            'education_code': 'level-1',
            'description': 'Level for test sale_crm_school',
            'short_description': 'L-1',
            'plan_id': self.education_plan.id}
        self.education_level = self.education_level_model.create(
            education_level_vals)
        sale_template = self.sale_template_model.search([], limit=1)
        education_course_vals = {
            'education_code': 'C1',
            'level_id': self.education_level.id,
            'description': 'Course 1'}
        self.education_course = self.education_course_model.create(
            education_course_vals)
        sale_template.write(
            {'course_id': self.education_course.id,
             'school_id': self.school.id})
        date_from = "{}-01-01".format(
            fields.Date.from_string(fields.Date.today()).year)
        date_from = fields.Date.from_string(date_from)
        date_to = "{}-12-31".format(
            int(fields.Date.from_string(fields.Date.today()).year)
            + 1)
        date_to = fields.Date.from_string(date_to)
        academic_year_vals = {
            'name': 'BBBBB2020',
            'date_start': date_from,
            'date_end': date_to}
        self.academic_year = self.academic_year_model.create(
            academic_year_vals)
        future_student_vals = {
            'name': 'Student for test sale_crm_school',
            'child_id': self.student.id,
            'birth_date': '2015-01-01',
            'gender': 'male',
            'school_id': self.school.id,
            'course_id': self.education_course.id,
            'academic_year_id': self.academic_year.id}
        lead_vals = {
            'name': 'Lead for test sale_crm_school',
            'partner_id': self.family.id,
            'future_student_ids': [(0, 0, future_student_vals)]}
        self.lead = self.lead_model.create(lead_vals)
        p = sale_template.sale_order_template_line_ids[0].product_id
        p.originator_id = 1
        family_vals = {
            'child2_id': self.student.id,
            'responsible_id': self.progenitor.id,
            'family_id': self.family.id,
            'payer': True,
            'payment_percentage': 100.0}
        self.family_obj.create(family_vals)

    def test_sale_crm_school(self):
        res = self.lead.create_sale_order_for_student()
        sale = self.sale_order_model.search(res.get('domain'))
        self.assertEqual(sale.child_id.id, self.student.id)
        self.assertEqual(len(sale.order_line[0].payer_ids), 1)
        sale.order_line[0].total_percentage = 50
        with self.assertRaises(ValidationError):
            sale.action_confirm()
        sale.order_line[0].total_percentage = 100.0
        sale.action_confirm()
        self.assertEqual(sale.state, 'sale')
