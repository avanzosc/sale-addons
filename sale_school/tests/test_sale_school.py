# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleSchoolCommon
from odoo.tests import common
from odoo.exceptions import ValidationError


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
        self.sale_order.action_confirm()

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
