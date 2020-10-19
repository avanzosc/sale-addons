# Copyright (c) 2020 Alfredo de la fuente - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderTemplatePrintSection(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderTemplatePrintSection, cls).setUpClass()
        cls.partner_model = cls.env['res.partner']
        cls.sale_model = cls.env['sale.order']
        template_vals = {
            'name': 'Name for TestSaleOrderTemplatePrintSection'}
        cls.product = cls.env.ref('product.consu_delivery_01')
        cls.product2 = cls.env.ref('product.consu_delivery_02')
        template_vals = {
            'name': 'Sale for test sale_stock_analytic',
            'partner_id': cls.env.ref('base.res_partner_12').id}
        template_line1_vals = {
            'product_id': cls.product.id,
            'name': 'Section 1',
            'display_type': 'line_section',
            'sequence': 10}
        template_line2_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom_id': cls.product.uom_id.id,
            'price_unit': 100,
            'sequence': 20}
        template_line3_vals = {
            'product_id': cls.product.id,
            'name': 'Section 2',
            'display_type': 'line_section',
            'sequence': 30}
        template_line4_vals = {
            'product_id': cls.product2.id,
            'name': cls.product2.name,
            'product_uom_qty': 5,
            'product_uom_id': cls.product2.uom_id.id,
            'price_unit': 25,
            'sequence': 40}
        template_vals['sale_order_template_line_ids'] = [
            (0, 0, template_line1_vals), (0, 0, template_line2_vals),
            (0, 0, template_line3_vals), (0, 0, template_line4_vals)]
        cls.template = cls.env['sale.order.template'].create(template_vals)
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.sale_order = cls.sale_model.create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,
        })

    def test_sale_order_template_print_section(self):
        line = self.template.mapped(
            'sale_order_template_line_ids').filtered(
                lambda x: x.name == 'Section 2')
        line.print_section_lines = False
        lines = self.template.mapped(
            'sale_order_template_line_ids').filtered(
                lambda x: x.print_section_lines)
        self.assertEquals(len(lines), 2)
        line = self.template.mapped(
            'sale_order_template_line_ids').filtered(
                lambda x: x.product_id == self.product2)
        line.sequence = 25
        lines = self.template.mapped(
            'sale_order_template_line_ids').filtered(
                lambda x: x.print_section_lines)
        self.assertEquals(len(lines), 3)

    def test_sale_order_print_section(self):
        self.assertEquals(0, len(self.sale_order.order_line))
        self.sale_order.sale_order_template_id = self.template.id
        self.sale_order.onchange_sale_order_template_id()
        self.assertEquals(4, len(self.sale_order.order_line))
        line = self.sale_order.mapped('order_line').filtered(
            lambda x: x.name == 'Section 2')
        line.print_section_lines = False
        lines = self.sale_order.mapped('order_line').filtered(
            lambda x: x.print_section_lines)
        self.assertEquals(len(lines), 2)
        line = self.sale_order.mapped('order_line').filtered(
            lambda x: x.product_id == self.product2)
        line.sequence = 25
        lines = self.sale_order.mapped('order_line').filtered(
            lambda x: x.print_section_lines)
        self.assertEquals(len(lines), 3)
