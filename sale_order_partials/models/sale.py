# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, exceptions, fields, models, _
from openerp.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    child_order_ids = fields.One2many(comodel_name="sale.order",
                                      inverse_name="parent_order_id",
                                      string="Sales")
    parent_order_id = fields.Many2one(comodel_name="sale.order")
    served_quantity = fields.Float(digits=dp.get_precision('Product Unit of '
                                                           'Measure'),
                                   compute="_compute_line_quantities")
    not_served_quantity = fields.Float(digits=dp.get_precision(
        'Product Unit of Measure'), compute="_compute_line_quantities")
    served_quantity_percentage = fields.Float(digits=dp.get_precision(
        'Product Unit of Measure'), compute="_compute_line_quantities")
    upgrade = fields.Boolean(string="Upgrade", copy=False)

    @api.multi
    def action_open_partial_sales(self):
        template_obj = self.env['product.template']
        result = template_obj._get_act_window_dict('sale.action_orders')
        result['domain'] = "[('parent_order_id', '=', %d)]" % self.id
        result['context'] = {'search_default_internal_loc': 1}
        return result

    @api.depends("order_line")
    def _compute_line_quantities(self):
        for record in self:
            if record.upgrade and record.order_line:
                total = record.order_line[0].product_uom_qty
                moves = record.child_order_ids.mapped(
                    'picking_ids.move_lines').filtered(
                        lambda x: x.state == 'confirmed')
                served_qty = sum(moves.mapped("product_uom_qty"))
                not_served_qty = total - served_qty
                record.served_quantity = served_qty
                record.not_served_quantity = not_served_qty
                record.served_quantity_percentage = (
                        served_qty / total * 100)

    @api.constrains("order_line", "upgrade")
    def check_sale_upgradable_has_one_line(self):
        if self.upgrade and len(self.order_line) > 1:
            raise exceptions.Warning('Sale upgrades can only have one '
                                     'order line')

    @api.onchange("upgrade")
    def onchange_upgrade(self):
        if self.upgrade:
            #TODO make to stock bezela markau
            pass

    @api.multi
    def action_create_order_from_upgrade(self, qty=None):
        param_obj = self.env['sale.config.settings']
        sale_type = param_obj._get_parameter('sale.type.id').value
        for record in self:
            if record.upgrade and record.invoiced:
                new_record = record.copy({'parent_order_id': record.id,
                                          'type_id': int(sale_type)})
                if qty:
                    new_record.order_line[0].write({'product_uom_qty': qty,
                                                    'discount': 100.})
            elif not record.upgrade:
                raise exceptions.Warning(
                    _("The order %s is not upgradable. Edit order and check "
                      "'Upgrade' field") % record.name)
            else:
                raise exceptions.Warning(_("There are unpaid invoices"))
