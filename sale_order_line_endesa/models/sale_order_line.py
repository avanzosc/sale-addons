# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import AccessError

# Fields that Endesa delivery managers fill in by hand.
ENDESA_EDITABLE_FIELDS = {
    "endesa_code",
    "endesa_state",
    "endesa_need_date",
    "endesa_id",
    "endesa_serial",
    "endesa_review",
}


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_endesa = fields.Boolean(related="order_id.is_endesa")
    endesa_code = fields.Char(
        copy=False, help="Code of the product in the Endesa catalog."
    )
    endesa_state = fields.Selection(
        selection=[
            ("PDP", "PDP"),
            ("PDI", "PDI"),
            ("CSV", "CSV"),
            ("QA", "QA"),
        ],
        copy=False,
    )
    endesa_need_date = fields.Datetime(copy=False)
    endesa_id = fields.Char(string="Endesa ID", copy=False)
    endesa_serial = fields.Char(string="Endesa S/N", copy=False)
    endesa_review = fields.Boolean(copy=False)
    endesa_date_color = fields.Selection(
        selection=[
            ("red", "Red"),
            ("orange", "Orange"),
            ("yellow", "Yellow"),
            ("ok", "OK"),
        ],
        compute="_compute_endesa_date_color",
        help="Color of the need date: red if it is due, orange if it is due "
        "in 7 days or less and yellow in 15 days or less. QA lines are not "
        "colored.",
    )
    endesa_can_edit = fields.Boolean(compute="_compute_endesa_can_edit")
    endesa_planned_date = fields.Datetime(
        string="Planned Date",
        related="order_id.commitment_date",
        store=True,
    )
    endesa_production_ids = fields.Many2many(
        comodel_name="mrp.production",
        string="Manufacturing Orders",
        compute="_compute_endesa_production",
        help="Manufacturing orders that supply the line: the ones its stock "
        "moves come from (make to order) and the ones with the line as origin.",
    )
    endesa_production_date = fields.Datetime(
        string="Manufacturing Date",
        compute="_compute_endesa_production",
        help="Latest end date of the manufacturing orders of the line.",
    )
    # Name of the delivery address alone, without its company in front.
    endesa_partner_short = fields.Char(
        string="Short Destination", related="order_id.partner_shipping_id.name"
    )
    order_partner_shipping_id = fields.Many2one(
        string="Destination", related="order_id.partner_shipping_id"
    )
    order_origin = fields.Char(string="Contract", related="order_id.origin")
    order_client_order_ref = fields.Char(
        string="Endesa Order", related="order_id.client_order_ref"
    )
    product_default_code = fields.Char(related="product_id.default_code")

    @api.depends("endesa_need_date", "endesa_state")
    def _compute_endesa_date_color(self):
        today = fields.Date.context_today(self)
        for line in self:
            color = "ok"
            if line.endesa_need_date and line.endesa_state != "QA":
                need_date = line.endesa_need_date.date()
                if need_date <= today:
                    color = "red"
                elif need_date <= today + relativedelta(days=7):
                    color = "orange"
                elif need_date <= today + relativedelta(days=15):
                    color = "yellow"
            line.endesa_date_color = color

    # order_id: so that it is also computed on new lines (onchange).
    @api.depends("order_id")
    @api.depends_context("uid")
    def _compute_endesa_can_edit(self):
        can_edit = self.env.user.has_group(
            "sale_order_line_endesa.group_endesa_manager"
        )
        for line in self:
            line.endesa_can_edit = can_edit

    @api.depends(
        "move_ids.move_orig_ids.production_id.date_finished",
        "move_ids.move_orig_ids.production_id.sale_line_id",
    )
    def _compute_endesa_production(self):
        # The make to order manufacturing orders are not linked to the line
        # (sale_line_id): they are reached through the chain of stock moves.
        origin_productions = self.env["mrp.production"].search(
            [("sale_line_id", "in", self._origin.ids)]
        )
        for line in self:
            moves = self.env["stock.move"].browse(line.move_ids._rollup_move_origs())
            productions = moves.production_id | origin_productions.filtered(
                lambda production, line=line: production.sale_line_id == line._origin
            )
            line.endesa_production_ids = productions
            line.endesa_production_date = max(
                productions.filtered("date_finished").mapped("date_finished"),
                default=False,
            )

    @api.onchange("endesa_need_date")
    def _onchange_endesa_need_date(self):
        if self.endesa_need_date:
            self.endesa_review = True

    def _check_endesa_access(self, vals_list):
        if self.env.su:
            return
        user = self.env.user
        if not user.has_group("sale_order_line_endesa.group_endesa_manager"):
            if any(ENDESA_EDITABLE_FIELDS & set(vals) for vals in vals_list):
                raise AccessError(
                    _("Only Endesa delivery managers can change the Endesa fields.")
                )
        elif not user.has_group("sales_team.group_sale_salesman"):
            # Their write access to the lines is only for the Endesa fields.
            if any(set(vals) - ENDESA_EDITABLE_FIELDS for vals in vals_list):
                raise AccessError(
                    _("Without access to Sales you can only change the Endesa fields.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        self._check_endesa_access(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        self._check_endesa_access([vals])
        return super().write(vals)
