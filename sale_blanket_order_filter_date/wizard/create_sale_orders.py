# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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

    def create_sale_order(self):
        min_date = False
        lines = self.line_ids.filtered(lambda x: x.date_schedule)
        if lines:
            line = min(lines, key=lambda x: x.date_schedule)
            min_date = line.date_schedule
        return super(
            BlanketOrderWizard, self.with_context(min_date=min_date)
        ).create_sale_order()

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
        if "min_date" in self.env.context and self.env.context.get("min_date", False):
            vals["commitment_date"] = self.env.context.get("min_date")
        return vals
