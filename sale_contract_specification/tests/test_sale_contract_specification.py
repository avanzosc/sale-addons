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

        cls.template = cls.env['sale.condition.template'].create({
            'name': 'Warranties',
        })
        cls.condition = cls.env['sale.condition'].create({
            'name': 'Warranty',
            'description': 'Products are guarantee by manufacturer',
            'template_ids': [(4, cls.template.id)],
        })

    def test_import(self):
        self.assertFalse(self.sale_order.condition_ids)
        self.assertFalse(self.sale_order.condition_tmpl_id)
        self.sale_order.condition_tmpl_id = self.template
        self.assertFalse(self.sale_order.condition_ids)
        self.sale_order._onchange_condition_tmpl_id()
        self.assertTrue(self.sale_order.condition_ids)
        self.assertEqual(len(self.sale_order.condition_ids),
                         len(self.template.condition_ids))
        self.sale_order._onchange_condition_tmpl_id()
        self.assertEqual(len(self.sale_order.condition_ids),
                         len(self.template.condition_ids) * 2)