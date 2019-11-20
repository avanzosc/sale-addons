# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields
from dateutil.relativedelta import relativedelta


class SaleOrderRentalCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrderRentalCommon, cls).setUpClass()
        cls.invoice_model = cls.env['account.invoice']

        cls.sale_model = cls.env['sale.order'].with_context(
            tracking_disable=True)
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
        })
        # cls.service_product = cls.env.ref('product.product_delivery_02')
        cls.customer = cls.env.ref('base.res_partner_1')
        cond = [('type_tax_use', '=', 'sale'),
                ('amount', '>', 1)]
        cls.tax = cls.env['account.tax'].search(cond, limit=1)
        cls.delivery_date = fields.Date.today()
        cls.end_date = cls.delivery_date + relativedelta(days=+6)
        cls.sale_order = cls.sale_model.create({
            'partner_id': cls.customer.id,
            'order_line': [(0, 0, {
                'product_id': cls.product.id,
                'name': cls.product.name,
                'product_uom_qty': 2,
                'product_uom': cls.product.uom_id.id,
                'price_unit': cls.product.list_price,
                'expected_delivery_date': cls.delivery_date,
                'expected_end_date': cls.end_date,
                'tax_id': [(6, 0, cls.tax.ids)],
            })]
        })
        cls.sale_order.warehouse_id.out_type_id.return_picking_type_id.\
            default_location_dest_id.write({
                'return_location': True,
            })
