# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.exceptions import UserError


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderLineAmountControl(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineAmountControl, cls).setUpClass()
        cond = [('state', '=', 'draft')]
        cls.sale = cls.env['sale.order'].search(cond, limit=1)

    def test_sale_order_line_amount_control(self):
        self.sale.order_line[0].write({'price_unit': 0.5})
        with self.assertRaises(UserError):
            self.sale.action_confirm()
