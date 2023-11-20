# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    ram_id = fields.Many2one(
        string="RAM", comodel_name="ram", related="lot_id.ram_id",
        copy=False, store=True,)
    storage1_size_id = fields.Many2one(
        string="Storage 1 Size", comodel_name="storage.size",
        related="lot_id.storage1_size_id", copy=False, store=True)
    grade_id = fields.Many2one(
        string="Grade", comodel_name="grade", copy=False, store=True,
        related="lot_id.grade_id")
    grade_tested = fields.Selection(
        string="Grade tested", related="lot_id.grade_tested", store=True,
        copy=False)
    allowed_lots_ids = fields.Many2many(
        string="Allowed lots", comodel_name="stock.production.lot",
        related="move_id.allowed_lots_ids")
