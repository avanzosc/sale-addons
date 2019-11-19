# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def button_open_lines(self):
        self.ensure_one()
        action = self.env.ref(
            'sale_order_line_input.action_sales_order_line_input')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'default_order_id': self.id,
            'default_order_partner_id': self.partner_id.id,
        })
        domain = expression.AND([
            [('order_id', 'in', self.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict
