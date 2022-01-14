# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_hour = fields.Float(string='Estimated Service Hours', default=0)
    price_hour = fields.Float(string='Estimated hour price', default=0)
    workforce_cost = fields.Float(
        string='Workforce Cost', compute='_compute_workforce_cost')
    material_cost = fields.Float(string='Material Cost')

    @api.depends('service_hour', 'price_hour')
    def _compute_workforce_cost(self):
        for product in self:
            product.workforce_cost = product.service_hour * product.price_hour

    @api.onchange('service_hour', 'price_hour', 'workforce_cost',
                  'material_cost')
    def onchange_standard_price(self):
        self.standard_price = self.workforce_cost + self.material_cost
