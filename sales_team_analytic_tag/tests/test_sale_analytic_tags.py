# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleAnalyticTags(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleAnalyticTags, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.tag_model = cls.env['account.analytic.tag']
        cls.team_model = cls.env['crm.team']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        SaleOrder = cls.env['sale.order'].with_context(tracking_disable=True)
        cls.tag1 = cls.tag_model.create({
            'name': 'Tag1'
        })
        cls.tag2 = cls.tag_model.create({
            'name': 'Tag2'
        })
        cls.team = cls.team_model.create({
            'name': 'Team 1',
            'team_type': 'sales',
            'analytic_tag_ids': [(6, 0, [cls.tag1.id, cls.tag2.id])]
        })
        cls.default_team = cls.env['crm.team']._get_default_team_id()
        cls.default_team.analytic_tag_ids = [cls.tag2.id]
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.sale_order = SaleOrder.create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
            'team_id': cls.team.id
        })

    def test_add_analytic_tags(self):
        line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 100,
            'order_id': self.sale_order.id
            }
        line = self.env['sale.order.line'].create(line_vals)
        self.assertEqual(line.analytic_tag_ids.ids,
                         self.team.analytic_tag_ids.ids)
        self.sale_order.team_id = self.default_team.id
