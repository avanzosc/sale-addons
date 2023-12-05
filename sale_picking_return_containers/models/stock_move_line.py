# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    picking_partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="picking_id.partner_id",
        store=True)
    max_return = fields.Float(
        string="Max. Qty to Return",
        related="move_id.purchase_line_id.max_return",
        store=True)
    returnable = fields.Boolean(
        string="Returnable",
        default=False,
        related="product_id.returnable",
        store=True)

    @api.constrains("max_return", "qty_done")
    def _check_max_return(self):
        for line in self:
            if line.product_id.returnable and line.max_return != 0 and (
                line.qty_done > line.max_return) and (
                    line.standard_price != 0):
                raise ValidationError(
                        _("The quantity can't be bigger than the maximum " +
                          "quantity to return."))
