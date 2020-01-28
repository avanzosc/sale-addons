# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.sale_school.tests.common import TestSaleSchoolCommon


class TestSaleSchoolGenerateSepaCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleSchoolGenerateSepaCommon, cls).setUpClass()
        payer_line = cls.sale_order.order_line[:1].payer_ids[:1]
        payer_line.write({
            "pay_percentage": 100.0,
        })
