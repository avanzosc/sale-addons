# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_devolution = fields.Boolean(default=False)

    def action_return_returnable(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("The supplier is not established"))
        for line in self.order_line.filtered(lambda c: (c.product_id.returnable)):
            line.unlink()
        sale_lines = (
            self.env["sale.order.line"]
            .search(
                [("order_partner_id", "=", self.partner_id.id), ("state", "=", "sale")]
            )
            .filtered(lambda c: c.pending_qty > 0 and c.product_id.returnable)
        )
        if not sale_lines:
            return
        processed = set()
        for line in sale_lines:
            key = (line.product_id.id, line.price_unit)
            if key in processed:
                continue
            processed.add(key)
            product_id, price_unit = key
            salelines = self.order_line.filtered(
                lambda c, pid=product_id, pu=price_unit: c.product_id.id == pid
                and c.price_unit == pu
            )
            if salelines:
                continue
            lines = sale_lines.filtered(
                lambda c, pid=product_id, pu=price_unit: c.product_id.id == pid
                and c.price_unit == pu
            )
            qty = sum(lines.mapped("pending_qty"))
            self.env["purchase.order.line"].create(
                {
                    "name": line.product_id.name,
                    "product_id": product_id,
                    "product_qty": qty,
                    "max_return": qty,
                    "price_unit": price_unit,
                    "price_subtotal": qty * price_unit,
                    "order_id": self.id,
                    "sale_order_line_ids": [(6, 0, lines.ids)],
                }
            )
