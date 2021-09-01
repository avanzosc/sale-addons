# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    count_attachments = fields.Integer(
        string='Attachments', compute='_compute_count_attachments')

    def _compute_count_attachments(self):
        for template in self:
            cond = [('res_model', '=', 'product.template'),
                    ('res_id', 'in', self.ids)]
            attachments = self.env['ir.attachment'].search(cond)
            template.count_attachments = len(attachments)

    def button_show_attachments(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id(
            'base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'product.template'),
                         ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'product.template',
                          'default_res_id': self.id}
        return res
