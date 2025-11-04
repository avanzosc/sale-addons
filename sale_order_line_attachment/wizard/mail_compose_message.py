# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _onchange_template_id(self, template_id, composition_mode, model,
                             res_id):
        attachment_obj = self.env['ir.attachment']
        result = super(MailComposeMessage, self)._onchange_template_id(
            template_id, composition_mode, model, res_id)
        value = (result.get('value') or {})
        attachment_ids = (value.get('attachment_ids') or [])

        if ('active_model' in self.env.context and
                self.env.context.get('active_model', 'a') == 'sale.order'):
            sale = self.env['sale.order'].browse(
                self.env.context.get('active_id'))
            for line in sale.order_line:
                cond = [('res_model', '=', 'sale.order.line'),
                        ('res_id', 'in', line.ids)]
                attachmets = attachment_obj.search(cond)
                for attachment in attachmets:
                    attachment_ids.append((4, attachment.id))
        value['attachment_ids'] = attachment_ids
        result['value']= value
        return result
