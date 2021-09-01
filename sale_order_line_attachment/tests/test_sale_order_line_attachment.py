# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
import base64


class TestSaleOrderLineAttachment(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineAttachment, cls).setUpClass()
        cls.mail_template = cls.env.ref('sale.email_template_edi_sale')
        cls.wiz_obj = cls.env['mail.compose.message']
        cls.sale_obj = cls.env['sale.order']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner sale order line attachment',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order line attachment',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id})
        cls.env['ir.attachment'].create({
            'name': 'Attach1',
            'datas': base64.b64encode(b"avanzosc1"),
            'res_model': 'product.template',
            'res_id': cls.product.product_tmpl_id.id,
            'attach_in_sales_orders': True})
        cls.env['ir.attachment'].create({
            'name': 'Attach2',
            'datas': base64.b64encode(b"avanzosc2"),
            'res_model': 'product.template',
            'res_id': cls.product.product_tmpl_id.id,
            'attach_in_sales_orders': True})
        cls.env['ir.attachment'].create({
            'name': 'Attach3',
            'datas': base64.b64encode(b"avanzosc3"),
            'res_model': 'product.template',
            'res_id': cls.product.product_tmpl_id.id,
            'attach_in_sales_orders': False})

    def test_sale_order_line_attachment(self):
        self.assertEqual(self.product.product_tmpl_id.count_attachments, 3)
        result = self.product.product_tmpl_id.button_show_attachments()
        domain = str(result.get('domain'))
        my_domain = "[('res_model', '=', 'product.template'), "\
                    "('res_id', 'in', [{}])]".format(
                        self.product.product_tmpl_id.id)
        self.assertEqual(domain, my_domain)
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 100}
        sale_vals = {
            "partner_id": self.partner.id,
            "partner_invoice_id": self.partner.id,
            "partner_shipping_id": self.partner.id,
            "company_id": self.company.id,
            "order_line": [(0, 0, sale_line_vals)]}
        sale = self.sale_obj.create(sale_vals)
        result = sale.order_line[0].action_get_attachment_view()
        domain = str(result.get('domain'))
        my_domain = "[('res_model', '=', 'sale.order.line'), "\
                    "('res_id', 'in', [{}])]".format(sale.order_line[0].id)
        self.assertEqual(domain, my_domain)
        wiz = self.wiz_obj.create({})
        result = wiz.with_context(
            active_model='sale.order', active_id=sale.id).onchange_template_id(
                self.mail_template.id, 'comment', 'sale.order', sale.id)
        value = result.get('value', {})
        attachments = value.get('attachment_ids', [])
        self.assertEqual(len(attachments), 3)
