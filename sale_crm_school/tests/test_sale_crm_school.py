# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import exceptions, fields


@common.at_install(False)
@common.post_install(True)
class TestSaleCrmSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleCrmSchool, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.lead_model = cls.env['crm.lead']
        cls.education_plan_model = cls.env['education.plan']
        cls.education_level_model = cls.env['education.level']
        cls.education_course_model = cls.env['education.course']
        cls.academic_year_model = cls.env['education.academic_year']
        cls.sale_template_model = cls.env['sale.order.template']
        cls.sale_order_model = cls.env['sale.order']
        cls.family_obj = cls.env['res.partner.family']
        school_vals = {
            'name': 'School for test sale_crm_school',
            'educational_category': 'school'}
        cls.school = cls.partner_model.create(school_vals)
        student_vals = {
            'name': 'Student for test sale_crm_school',
            'educational_category': 'student'}
        cls.student = cls.partner_model.create(student_vals)
        family_vals = {
            'name': 'Family for test sale_crm_school',
            'educational_category': 'family'}
        cls.family = cls.partner_model.create(family_vals)
        progenitor_vals = {
            'name': 'Progenitor for test sale_crm_school',
            'educational_category': 'progenitor'}
        cls.progenitor = cls.partner_model.create(progenitor_vals)
        education_plan_vals = {
            'description': 'Education plan for test sale_crm_school',
            'education_code': 'code-1'}
        cls.education_plan = cls.education_plan_model.create(
            education_plan_vals)
        education_level_vals = {
            'education_code': 'level-1',
            'description': 'Level for test sale_crm_school',
            'short_description': 'L-1',
            'plan_id': cls.education_plan.id}
        cls.education_level = cls.education_level_model.create(
            education_level_vals)
        sale_template = cls.sale_template_model.search([], limit=1)
        education_course_vals = {
            'education_code': 'C1',
            'level_id': cls.education_level.id,
            'description': 'Course 1'}
        cls.education_course = cls.education_course_model.create(
            education_course_vals)
        sale_template.write(
            {'course_id': cls.education_course.id,
             'school_id': cls.school.id})
        today = fields.Date.today()
        date_from = today.replace(month=1, day=1)
        date_to = today.replace(year=today.year + 1, month=12, day=31)
        cls.academic_year_vals = {
            'name': '{}-{}'.format(date_to.year, date_from.year),
            'date_start': date_from,
            'date_end': date_to,
        }
        future_student_vals = {
            'name': 'Student for test sale_crm_school',
            'child_id': cls.student.id,
            'birth_date': '2015-01-01',
            'gender': 'male',
            'school_id': cls.school.id,
            'course_id': cls.education_course.id,
        }
        lead_vals = {
            'name': 'Lead for test sale_crm_school',
            'partner_id': cls.family.id,
            'future_student_ids': [(0, 0, future_student_vals)]}
        cls.lead = cls.lead_model.create(lead_vals)
        p = sale_template.sale_order_template_line_ids[0].product_id
        p.originator_id = 1
        family_vals = {
            'child2_id': cls.student.id,
            'responsible_id': cls.progenitor.id,
            'family_id': cls.family.id,
            'payer': True,
            'payment_percentage': 100.0}
        cls.family_obj.create(family_vals)

    def test_sale_crm_school(self):
        with self.assertRaises(exceptions.Warning):
            self.lead.create_sale_order_for_student()
        academic_year = self.academic_year_model.create(
            self.academic_year_vals)
        with self.assertRaises(exceptions.Warning):
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
        for sale in sales:
            self.assertEquals(sale.state, 'draft')
            line = sale.order_line[:1]
            self.assertEquals(len(line.payer_ids), 1)
            payer_line = line.payer_ids[:1]
            self.assertEquals(payer_line.child_id, sale.child_id)
            self.assertIn(payer_line.payer_id, payer_line.allowed_payers_ids)
            payer_line.pay_percentage = 50.0
            self.assertNotEquals(line.total_percentage, 100.0)
            with self.assertRaises(exceptions.ValidationError):
                sale.action_confirm()
            payer_line.pay_percentage = 100.0
            self.assertEquals(line.total_percentage, 100.0)
            sale.action_confirm()
            self.assertNotEquals(sale.state, 'draft')
