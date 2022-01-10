# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    workforce_cost = fields.Float(
        string='Workforce Cost')
    material_cost = fields.Float(string='Material Cost')
    standard_price = fields.Float(
        string='Standard Cost',
        related='product_id.standard_price', store=True)
    cost_unit = fields.Float(string='Cost Unit')
    cost_subtotal = fields.Float(string='Cost Subtotal')

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.workforce_cost = self.product_id.workforce_cost
        self.material_cost = self.product_id.material_cost

    @api.onchange('workforce_cost', 'material_cost')
    def onchange_cost_unit(self):
        self.cost_unit = self.workforce_cost + self.material_cost

    @api.onchange('cost_unit', 'product_uom_qty')
    def onchange_price_subtotal(self):
        self.cost_subtotal = self.product_uom_qty * self.cost_unit
