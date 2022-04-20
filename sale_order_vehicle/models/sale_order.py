# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vehicle_id = fields.Many2one(
        string='Vehicle',
        comodel_name='fleet.vehicle')

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        if self.project_id:
            self.project_id.vehicle_id = self.vehicle_id.id
        return result
