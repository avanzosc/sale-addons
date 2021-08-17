# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.sale_school.tests.common import \
    TestSaleSchoolCommon


class TestSaleHrSchoolCommon(TestSaleSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestSaleHrSchoolCommon, cls).setUpClass()
        cls.supervised_model = cls.env["hr.employee.supervised.year"]
        cls.progenitor.write({
            "customer_payment_mode_id": cls.payment_mode.id,
        })
        payer_line = cls.sale_order.order_line[:1].payer_ids[:1]
        payer_line.write({
            "pay_percentage": 100.0,
        })
        payer_line._onchange_payer_id()
