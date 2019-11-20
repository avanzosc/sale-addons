# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestSaleSchoolCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleSchoolCommon, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.sale_order_model = cls.env['sale.order']
        cls.product_model = cls.env['product.product']
        cls.family_obj = cls.env['res.partner.family']
        school_vals = {
            'name': 'School for test sale_school_generate_sepa',
            'educational_category': 'school'}
        cls.school = cls.partner_model.create(school_vals)
        student_vals = {
            'name': 'Student for test sale_school_generate_sepa',
            'educational_category': 'student'}
        cls.student = cls.partner_model.create(student_vals)
        family_vals = {
            'name': 'Family for test sale_school_generate_sepa',
            'educational_category': 'family'}
        cls.family = cls.partner_model.create(family_vals)
        progenitor_vals = {
            'name': 'Progenitor for test sale_school_generate_sepa',
            'educational_category': 'progenitor',
            'bank_ids': [(0, 0, {'acc_number': '123456789'})]}
        cls.progenitor = cls.partner_model.create(progenitor_vals)
        family_vals = {
            'child2_id': cls.student.id,
            'responsible_id': cls.progenitor.id,
            'family_id': cls.family.id,
            'payer': True,
            'payment_percentage': 100.0}
        cls.family_obj.create(family_vals)
        cls.service = cls.product_model.create({
            'name': 'Test Service'
        })
        cls.sale_order = cls.sale_order_model.create({
            'partner_id': cls.student.id,
            'order_line': [(0, 0, {
                'product_id': cls.service.id,
                'payer_ids': [(0, 0, {
                    'payer_id': cls.progenitor.id,
                    'pay_percentage': 100.0,
                })]
            })]
        })
