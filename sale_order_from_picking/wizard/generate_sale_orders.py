# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2020 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class GenerateSaleOrdersWizard(models.TransientModel):
    _name = 'generate.sale.orders.wizard'
    _description = 'Generate multiple sale orders'

    def _check_pickings(self, picking_ids):
        picking_obj = self.env['stock.picking']
        fail_1 = picking_obj.search([('sale_order_id', '!=', False),
                                     ('id', 'in', picking_ids)])
        if fail_1:
            raise ValidationError(
                _('There are already generated sale orders in selected '
                  'pickings.'))
        fail_2 = picking_obj.search([('picking_type_code', '!=', 'incoming'),
                                     ('id', 'in', picking_ids)])
        if fail_2:
            raise ValidationError(
                _('You can only generate sale orders from "incoming" '
                  'pickings.'))

    def generate_sale_orders(self):
        picking_obj = self.env['stock.picking']
        sale_obj = self.env['sale.order']
        info_obj = self.env['generated.message.wizard']
        self._check_pickings(self.env.context['active_ids'])
        sale_num = 0
        sale_orders = []
        pickings = []
        for picking_id in self.env.context['active_ids']:
            picking = picking_obj.browse(picking_id)
            sale_id = picking.create_sale_order()['res_id']
            sale_orders.append(sale_id)
            sale_num += 1
        # confirm sale_order
        for sale_id in sale_orders:
            sale = sale_obj.browse(sale_id)
            sale.action_confirm()
            pickings.extend(sale.picking_ids.ids)
        # process pickings
        for picking_id in pickings:
            pick = picking_obj.browse(picking_id)
            wiz_act = pick.button_validate()
            wiz = self.env[wiz_act['res_model']].browse(wiz_act['res_id'])
            wiz.process()
        message_id = info_obj.create(
            {'message': _("Number of generated sale orders: %s" % sale_num)})
        return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'generated.message.wizard',
            # pass the id
            'res_id': message_id.id,
            'target': 'new'
        }


class GeneratedMessageWizard(models.TransientModel):
    _name = 'generated.message.wizard'
    _description = 'Message Wizard'

    message = fields.Text('Message', required=True)
