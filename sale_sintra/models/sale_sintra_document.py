# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleSintraDocument(models.Model):
    _name = "sale.sintra.document"
    _description = "Sintra Document"

    sintra_id = fields.Many2one(
        comodel_name="sale.sintra", string="Sintra", required=True, ondelete="cascade"
    )
    name = fields.Char(string="Document")
    folder = fields.Text(default="/in/Documentacion/Ocr_Sintra")
    note = fields.Text(copy=False)
