# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    ram_id = fields.Many2one(string="RAM", comodel_name="ram", copy=False)
    storage1_size_id = fields.Many2one(
        string="Storage 1 Size", comodel_name="storage.size", copy=False
    )
    grade_id = fields.Many2one(string="Grade", comodel_name="grade")
    grade_tested = fields.Selection(
        string="Grade tested", related="grade_id.tested", store=True, copy=False
    )
