# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    ram_id = fields.Many2one(
        string="RAM",
        comodel_name="ram",
        related="sale_line_id.ram_id",
        copy=False,
        store=True,
    )
    storage1_size_id = fields.Many2one(
        string="Storage 1 Size",
        comodel_name="storage.size",
        related="sale_line_id.storage1_size_id",
        copy=False,
        store=True,
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="grade",
        copy=False,
        store=True,
        related="sale_line_id.grade_id",
    )
    grade_tested = fields.Selection(
        string="Grade tested",
        related="sale_line_id.grade_tested",
        store=True,
        copy=False,
    )
    allowed_lots_ids = fields.Many2many(
        string="Allowed lots",
        comodel_name="stock.production.lot",
        compute="_compute_allowed_lots",
    )

    def _update_reserved_quantity(
        self,
        need,
        available_quantity,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=True,
    ):
        self.ensure_one()
        return super(
            StockMove, self.with_context(origin_move=self)
        )._update_reserved_quantity(
            need,
            available_quantity,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )

    def _get_available_quantity(
        self,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        allow_negative=False,
    ):
        self.ensure_one()
        return super(
            StockMove, self.with_context(origin_move=self)
        )._get_available_quantity(
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
            allow_negative=allow_negative,
        )

    def _compute_allowed_lots(self):
        for move in self:
            lots = False
            quants = (
                self.env["stock.quant"]
                .with_context(origin_move=move)
                ._gather(move.product_id, move.location_id)
            )
            if quants:
                lots = quants.mapped("lot_id")
            move.allowed_lots_ids = [(6, 0, lots.ids)] if lots else []
