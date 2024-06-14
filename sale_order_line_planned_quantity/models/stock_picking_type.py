# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    use_to_calculate_planned_quantities = fields.Boolean(
        string="Use To Calculate Planned Quantities", default=False,
        copy=False
    )
