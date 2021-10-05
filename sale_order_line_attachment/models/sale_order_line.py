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
