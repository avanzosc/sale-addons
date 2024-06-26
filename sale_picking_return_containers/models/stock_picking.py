# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    no_upadate_returns = fields.Boolean(string="No update return", default=False)

    def button_validate(self):
        for picking in self:
            lines = picking.move_line_ids_without_package.filtered(
                lambda c: c.qty_done != 0
            )
            if not lines:
                picking.button_force_done_detailed_operations()
            result = super(StockPicking, self).button_validate()
            if picking.picking_type_code == ("incoming") and not (
                picking.no_upadate_returns
            ):
                for line in picking.move_ids_without_package.filtered(
                    lambda c: (c.product_id.returnable)
                ):
                    if (
                        line
                        and (line.purchase_line_id)
                        and (line.purchase_line_id.sale_order_line_ids)
                    ):
                        qty = line.quantity_done
                        i = 0
                        sales = line.purchase_line_id.sale_order_line_ids.sorted(
                            "create_date"
                        )
                        sale_line = []
                        while qty > 0 and i < len(sales):
                            sale_line.append(sales[i].id)
                            pending = sales[i].pending_qty
                            returned = sales[i].returned_amount
                            if qty <= pending:
                                returned += qty
                                pending -= qty
                                qty = 0
                            else:
                                returned += pending
                                qty -= pending
                                pending = 0
                            sales[i].write(
                                {"returned_amount": returned, "pending_qty": pending}
                            )
                            i += 1
                        if qty > 0:
                            pending_negative = self.env["sale.order.line"].search(
                                [
                                    (
                                        "order_partner_id",
                                        "=",
                                        line.picking_id.partner_id.id,
                                    ),
                                    ("state", "=", "sale"),
                                    ("product_id", "=", line.product_id.id),
                                    ("pending_qty", "<", 0),
                                    ("price_unit", "=", 0),
                                ],
                                limit=1,
                            )
                            if not pending_negative:
                                pending_negative = sales[i - 1]
                            pending_negative.pending_qty -= qty
                            pending_negative.returned_amount += qty
                        line.purchase_line_id.sale_order_line_ids = [(6, 0, sale_line)]
                    picking.no_upadate_returns = True
            elif picking.picking_type_code == "outgoing":
                for line in picking.move_ids_without_package.filtered(
                    lambda c: (c.product_id.returnable)
                ):
                    qty = line.quantity_done
                    while qty > 0:
                        pending_negative = self.env["sale.order.line"].search(
                            [
                                (
                                    "order_partner_id",
                                    "=",
                                    line.picking_id.partner_id.id,
                                ),
                                ("state", "=", "sale"),
                                ("product_id", "=", line.product_id.id),
                                ("pending_qty", "<", 0),
                                ("price_unit", "=", 0),
                            ],
                            limit=1,
                        )
                        if pending_negative and abs(pending_negative.pending_qty) >= (
                            qty
                        ):
                            pending_negative.pending_qty += qty
                            qty = 0
                        elif pending_negative and abs(pending_negative.pending_qty) < (
                            qty
                        ):
                            qty += pending_negative.pending_qty
                            pending_negative.pending_qty = 0
                        elif not pending_negative:
                            line.sale_line_id.pending_qty = qty
                            qty = 0
            elif picking.picking_type_code == ("incoming") and (
                picking.no_upadate_returns
            ):
                picking.no_upadate_returns = False
            return result
