# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class SaleOrderPartials(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrderPartials, cls).setUpClass()
        cls.wiz_obj = cls.env['duplicate.upgradable.sale']
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner to test',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product to test'
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'upgrade': True,
            'order_line': [(0, 0, {'product_id': cls.product.id,
                                   'product_uom_qty': 100}, )],
        })

    def test_partials(self):
        wiz = self.wiz_obj.with_context(active_ids=[
            self.sale_order.id]).create({
                'quantity': 5})
        with self.assertRaises(exceptions.Warning):
            wiz.action_duplicate()
