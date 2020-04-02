# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleLinePendingInfo(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleLinePendingInfo, cls).setUpClass()
        cls.sale_model = cls.env['sale.order']
        cls.report_model = cls.env['sale.report']

    def test_sale_line_pending_info(self):
        cond = [('state', 'in', ('sale', 'done'))]
        sale = self.sale_model.search(cond, limit=1)
        sale.order_line.write({'discount': 5})
        for line in sale.order_line:
            self.assertEquals(line.qty_pending_delivery,
                              line.product_uom_qty - line.qty_delivered)
            amount = line.qty_pending_delivery * line.price_unit
            if line.discount:
                amount -= (amount * line.discount) / 100
            self.assertEquals(line.amount_pending_delivery, amount)
            self.assertEquals(line.qty_pending_invoicing,
                              line.product_uom_qty - line.qty_invoiced)
            amount = line.qty_pending_invoicing * line.price_unit
            if line.discount:
                amount -= (amount * line.discount) / 100
            self.assertEquals(line.amount_pending_invoicing, amount)
        self.assertEquals(
            sale.total_qty_pending_delivery,
            sum(sale.order_line.mapped('qty_pending_delivery')))
        self.assertEquals(
            sale.total_amount_pending_delivery,
            sum(sale.order_line.mapped('amount_pending_delivery')))
        self.assertEquals(
            sale.total_qty_pending_invoicing,
            sum(sale.order_line.mapped('qty_pending_invoicing')))
        self.assertEquals(
            sale.total_amount_pending_invoicing,
            sum(sale.order_line.mapped('amount_pending_invoicing')))
        res = self.report_model._query(
            with_clause='', fields=None, groupby='', from_clause='')
        self.assertIn('as qty_pending_delivery', res)
        self.assertIn('as qty_pending_invoicing', res)
        self.assertIn('as amount_pending_delivery', res)
        self.assertIn('as amount_pending_invoicing', res)
