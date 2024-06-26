# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPicking(models.Model):
    _inherit = "stock.picking"

    count_analytic_lines = fields.Integer(
        string="Count analytic lines", compute="_compute_count_analytic_lines"
    )

    def _compute_count_analytic_lines(self):
        for picking in self:
            picking.count_analytic_lines = len(picking._get_count_analytic_lines())

    def action_analytic_movements_from_picking(self):
        lines = self._get_count_analytic_lines()
        if lines:
            action = self.env.ref("analytic.account_analytic_line_action_entries")
            action_dict = action and action.read()[0]
            action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
            domain = expression.AND(
                [[("id", "in", lines.ids)], safe_eval(action.domain or "[]")]
            )
            action_dict.update({"domain": domain})
            return action_dict

    def _get_count_analytic_lines(self):
        lines = self.env["account.analytic.line"]
        if self.analytic_account_id:
            cond = [
                ("account_id", "=", self.analytic_account_id.id),
                ("partner_id", "=", self.partner_id.id),
            ]
            lines = self.env["account.analytic.line"].search(cond)
        return lines

    def create_analytic_line_from_out_picking(self):
        pickings = self.filtered(
            lambda x: x.picking_type_code == "outgoing"
            and x.state == "done"
            and x.analytic_account_id
        )
        for picking in pickings:
            for move in picking.move_ids_without_package:
                picking = move.picking_id
                if move.quantity_done > 0:
                    cond = [
                        ("stock_move_id", "=", move.id),
                        ("account_id", "=", picking.analytic_account_id.id),
                        ("partner_id", "=", picking.partner_id.id),
                        ("product_id", "=", move.product_id.id),
                        ("unit_amount", "<", 0),
                    ]
                    old_move = self.env["account.analytic.line"].search(cond, limit=1)
                    if not old_move:
                        vals = move._prepare_data_for_create_analytic_line()
                        if vals:
                            self.env["account.analytic.line"].create(vals)
