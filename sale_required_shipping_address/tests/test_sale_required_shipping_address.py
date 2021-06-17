# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleRequiredShippingAddress(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleRequiredShippingAddress, cls).setUpClass()
        cls.sale_model = cls.env['sale.order']
        cls.partner_model = cls.env['res.partner']
        vals = {'name': 'Company 1',
                'company_type': 'company'}
        cls.partner = cls.partner_model.create(vals)
        vals = {'name': 'Company 1 shipping address 1',
                'company_type': 'person',
                'type': 'delivery',
                'parent_id': cls.partner.id}
        cls.shipping1 = cls.partner_model.create(vals)
        vals = {'name': 'Company 1 shipping address 2',
                'company_type': 'person',
                'type': 'delivery',
                'parent_id': cls.partner.id}
        cls.shipping2 = cls.partner_model.create(vals)

    def test_sale_required_shipping_address(self):
        cond = [('state', '=', 'draft')]
        sale = self.sale_model.search(cond, limit=1)
        sale.partner_id = self.partner.id
        sale.onchange_partner_id()
        self.assertEqual(len(sale.allowed_shipping_ids), 3)
        result = sale.onchange_partner_id_warning()
        self.assertIn('warning', result)
        self.partner.write(
            {'sale_warn': 'warning',
             'sale_warn_msg': 'bbbbbb'})
        result = sale.onchange_partner_id_warning()
        warning = result.get('warning')
        message = warning.get('message')
        self.assertIn('bbbbbb', message)
