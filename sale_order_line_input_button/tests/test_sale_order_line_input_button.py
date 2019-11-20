# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.addons.sale.tests.test_sale_order import TestSaleOrder


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderLineInputButton(TestSaleOrder):

    def test_sale_order_button(self):
        action_dict = self.sale_order.button_open_lines()
        self.assertEquals(
            action_dict['context'].get('default_order_id'),
            self.sale_order.id)
        self.assertEquals(
            action_dict['context'].get('default_order_partner_id'),
            self.sale_order.partner_id.id)
        self.assertIn(
            ('order_id', 'in', self.sale_order.ids),
            action_dict.get('domain'))
