# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import api, exceptions, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_order_id = fields.Many2one(comodel_name='sale.order',
                                    string='Generated sale Order')

    @api.multi
    def create_sale_order(self):
        self.ensure_one()
        if not self.partner_id:
            raise exceptions.Warning(_("Partner not defined"))
        sale_obj = self.env['sale.order']
        sale_line_obj = self.env['sale.order.line']
        sale = sale_obj.create({'partner_id': self.partner_id.id})
        for line in self.move_lines:
            sale_line_data = {
                'product_id': line.product_id.id,
                'name': line.name,
                'uom_id': line.product_id.uom_id.id,
                'product_uom_qty': line.product_uom_qty,
                'order_id': sale.id,
                'stock_move_id': line.id,
                }
            sale_line_obj.create(sale_line_data)
        self.sale_order_id = sale.id
        view = self.env.ref('sale.view_order_form')
        return {
            'name': _('View Sale'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'fullscreen',
            'res_id': sale.id,
            'context': self.env.context,
        }
