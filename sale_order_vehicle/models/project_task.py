# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    vehicle_id = fields.Many2one(
        string='Vehicle',
        comodel_name='fleet.vehicle',
        related='sale_order_id.vehicle_id',
        store=True)
