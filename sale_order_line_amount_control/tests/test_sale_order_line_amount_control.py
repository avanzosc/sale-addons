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
        cond = [('state', '=', 'draft'),
                ('id', '!=', cls.sale.id)]
        cls.sale2 = cls.env['sale.order'].search(cond, limit=1)

    def test_sale_order_line_amount_control(self):
        self.sale2.order_line[0].write({'price_unit': 1})
        self.sale2.action_confirm()
        self.assertEqual(self.sale2.state, 'sale')
        self.sale.order_line[0].write({'price_unit': 1})
        with self.assertRaises(UserError):
            self.sale.with_context(check_amount_less=True).action_confirm()
