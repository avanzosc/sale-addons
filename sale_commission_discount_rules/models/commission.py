# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleCommission(models.Model):
    _inherit = "commission"

    commission_type = fields.Selection(
        selection_add=[("filter", "Filter")],
        ondelete={"filter": "set default"},
    )
    formula_data_ids = fields.Many2many(
        comodel_name="fcf.formula_data",
        string="Formula data",
        default=[],
    )
