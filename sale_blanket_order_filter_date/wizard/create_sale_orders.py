# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    @api.model
    def _default_lines_filter_date(self):
        line_obj = self.env["sale.blanket.order.line"]
        lines = self._default_lines()
        filtered_lines = []
        for line in lines:
            line_info = line[2]
            blanket_line = line_obj.browse(line_info.get("blanket_line_id"))
            valid = True
            if (
                blanket_line.order_id.date_from
                and blanket_line.date_schedule
                and blanket_line.date_schedule < blanket_line.order_id.date_from
            ) or (
                blanket_line.order_id.date_to
                and blanket_line.date_schedule
                and blanket_line.date_schedule > blanket_line.order_id.date_to
            ):
                valid = False
            if valid:
                filtered_lines.append(line)
        return filtered_lines

    line_ids = fields.One2many(
        default=_default_lines_filter_date,
    )

    def create_sale_order_by_date(self):
        dates = set(self.line_ids.mapped("date_schedule"))
        new_sales = []
        for date in dates:
            result = self.with_context(sale_blanker_order_date=date).create_sale_order()
            if "domain" in result:
                domain = result.get("domain")
                new_sales += domain[0][2]
        return {
            "domain": [("id", "in", new_sales)],
            "name": _("Sales Orders"),
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "context": {"from_sale_order": True},
            "type": "ir.actions.act_window",
        }

    def _prepare_so_vals(
        self,
        customer,
        user_id,
        currency_id,
        pricelist_id,
        payment_term_id,
        order_lines_by_customer,
    ):
        vals = super()._prepare_so_vals(
            customer,
            user_id,
            currency_id,
            pricelist_id,
            payment_term_id,
            order_lines_by_customer,
        )
        if "sale_blanker_order_date" in self.env.context:
            vals["commitment_date"] = self.env.context.get("sale_blanker_order_date")
        return vals

    def _prepare_so_line_vals(self, line):
        vals = super()._prepare_so_line_vals(line)
        if (
            "sale_blanker_order_date" in self.env.context
            and line.date_schedule == self.env.context.get("sale_blanker_order_date")
        ):
            vals["commitment_date"] = self.env.context.get("sale_blanker_order_date")
        return vals
