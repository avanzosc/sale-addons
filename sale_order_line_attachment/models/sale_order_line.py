# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id(
            'base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'sale.order.line'),
                         ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'sale.order.line',
                          'default_res_id': self.id}
        return res

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        line._catch_product_attachments()
        return line

    @api.multi
    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        if 'product_id' in vals and vals.get('product_id', False):
            for line in self:
                line._catch_product_attachments()
        return result

    def _catch_product_attachments(self):
        cond = [('res_model', '=', 'sale.order.line'),
                ('res_id', 'in', self.product_id.product_tmpl_id.ids)]
        attachments = self.env['ir.attachment'].search(cond)
        if attachments:
            attachments.unlink()
        cond = [('attach_in_sales_orders', '=', True),
                ('res_model', '=', 'product.template'),
                ('res_id', 'in', self.product_id.product_tmpl_id.ids)]
        attachments = self.env['ir.attachment'].search(cond)
        for attachment in attachments:
            attachment.copy(
                {'res_model': 'sale.order.line',
                 'res_id': self.id})
