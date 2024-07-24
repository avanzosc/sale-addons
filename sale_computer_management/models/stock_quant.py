# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    ram_id = fields.Many2one(
        string="RAM",
        comodel_name="ram",
        related="lot_id.ram_id",
        copy=False,
        store=True,
    )
    storage1_size_id = fields.Many2one(
        string="Storage 1 Size",
        comodel_name="storage.size",
        related="lot_id.storage1_size_id",
        copy=False,
        store=True,
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="grade",
        copy=False,
        store=True,
        related="lot_id.grade_id",
    )
    grade_tested = fields.Selection(
        string="Grade tested", related="lot_id.grade_tested", store=True, copy=False
    )

    def _gather(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
    ):
        quants = super(StockQuant, self)._gather(
            product_id,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )
        if "origin_move" not in self.env.context:
            return quants
        if quants:
            quants = quants.filtered(
                lambda x: x.grade_tested and x.grade_tested == "ok"
            )
        move = self.env.context.get("origin_move")
        if not move.ram_id and not move.storage1_size_id and not move.grade_id:
            return quants
        if quants and move.ram_id:
            quants = quants.filtered(lambda x: x.ram_id and x.ram_id == move.ram_id)
        if quants and move.storage1_size_id:
            quants = quants.filtered(
                lambda x: x.storage1_size_id
                and x.storage1_size_id == move.storage1_size_id
            )
        if quants and move.grade_id:
            quants = quants.filtered(
                lambda x: x.grade_id
                and x.grade_tested
                and x.grade_id == move.grade_id
                and x.grade_tested == "ok"
            )
        return quants
