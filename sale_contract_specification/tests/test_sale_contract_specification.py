# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo.tests import common


class TestSaleContractSpecification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleContractSpecification, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
        })
        cls.template1 = cls.env['contract.condition.template'].create({
            'name': 'Warranties',
        })
        cls.condition1 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'template_ids': [(4, cls.template1.id)],
        })
        cls.template2 = cls.env['contract.condition.template'].create({
            'name': 'Warranties',
        })
        cls.condition2 = cls.env['contract.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'template_ids': [(4, cls.template2.id)],
        })

    def test_draft_order(self):
        self.assertFalse(self.sale_order.draft_condition_ids)
        self.assertFalse(self.sale_order.draft_condition_tmpl_id)
        self.sale_order.draft_condition_tmpl_id = self.template1
        self.assertFalse(self.sale_order.draft_condition_ids)
        self.sale_order._onchange_draft_condition_tmpl_id()
        self.assertTrue(self.sale_order.draft_condition_ids)
        self.assertEqual(len(self.sale_order.draft_condition_ids),
                         len(self.template1.condition_ids))
        self.sale_order.draft_condition_tmpl_id = self.template2
        self.sale_order._onchange_draft_condition_tmpl_id()
        self.assertEqual(len(self.sale_order.draft_condition_ids),
                         (2 * len(self.template1.condition_ids)) +
                         len(self.template2.condition_ids))

    def test_sale_order(self):
        self.assertFalse(self.sale_order.condition_ids)
        self.assertFalse(self.sale_order.condition_tmpl_id)
        self.sale_order.condition_tmpl_id = self.template1
        self.assertFalse(self.sale_order.condition_ids)
        self.sale_order._onchange_condition_tmpl_id()
        self.assertTrue(self.sale_order.condition_ids)
        self.assertEqual(len(self.sale_order.condition_ids),
                         len(self.template1.condition_ids))
        self.sale_order.condition_tmpl_id = self.template2
        self.sale_order._onchange_condition_tmpl_id()
        self.assertEqual(len(self.sale_order.condition_ids),
                         (2 * len(self.template1.condition_ids)) +
                         len(self.template2.condition_ids))

    def test_draft_order_condition_name(self):
        self.sale_order.draft_condition_ids = [
            (0, 0, {'condition_id': self.condition1.id,
                    'description': self.condition1.name})]
        for condition in self.sale_order.draft_condition_ids:
            self.assertEquals(condition.display_name,
                              '[{}] {}'.format(condition.sale_id.name,
                                               condition.condition_id.name))

    def test_sale_order_condition_name(self):
        self.sale_order.condition_ids = [
            (0, 0, {'condition_id': self.condition1.id,
                    'description': self.condition1.name})]
        for condition in self.sale_order.condition_ids:
            self.assertEquals(condition.display_name,
                              '[{}] {}'.format(
                                  condition.sale_id.name,
                                  condition.condition_id.name))
