# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleSchoolCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleSchool(TestSaleSchoolCommon):

    def test_sale_school(self):
        payer = self.sale_order.mapped('order_line.payer_ids')[:1]
        self.assertEquals(
            payer.display_name,
            "{} ({} %)".format(payer.payer_id.name, payer.pay_percentage))
