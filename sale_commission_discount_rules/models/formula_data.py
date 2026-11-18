# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class FormulaData(models.Model):
    _name = "fcf.formula_data"
    _description = "Formula Data"

    category = fields.Many2one(comodel_name="product.category", required=True)
    operation = fields.Selection(
        selection=[
            ("==", "=="),
            (">", ">"),
            ("<", "<"),
            (">=", ">="),
            ("<=", "<="),
        ],
        required=True,
    )
    discount = fields.Float(required=True)
    commission = fields.Float(required=True)
