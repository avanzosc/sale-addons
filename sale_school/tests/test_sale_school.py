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
