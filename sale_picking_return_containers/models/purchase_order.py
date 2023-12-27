# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_devolution = fields.Boolean(
        string="Is Devolution",
        default=False
    )

    def action_return_returnable(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("The supplier is not established"))
        for line in self.order_line.filtered(
            lambda c: (
                c.product_id.returnable)):
            line.unlink()
        sale_lines = self.env["sale.order.line"].search([
            ("order_partner_id", "=", self.partner_id.id),
            ("state", "=", "sale")]).filtered(
                lambda c: c.pending_qty > 0 and c.product_id.returnable)
        if sale_lines:
            for line in sale_lines:
                salelines = self.order_line.filtered(
                    lambda c: c.product_id == line.product_id and (
                        c.price_unit == line.price_unit))
                if not salelines:
                    lines = sale_lines.filtered(
                        lambda c: c.product_id == line.product_id and (
                            c.price_unit == line.price_unit))
                    self.env["purchase.order.line"].create({
                        "name": line.product_id.name,
                        "product_id": line.product_id.id,
                        "product_qty": sum(lines.mapped("pending_qty")),
                        "max_return": sum(lines.mapped("pending_qty")),
                        "price_unit": line.price_unit,
                        "price_subtotal": sum(
                            lines.mapped("pending_qty")) * line.price_unit,
                        "order_id": self.id,
                        "sale_order_line_ids": [(6, 0, lines.ids)]})

    def action_create_invoice(self):
        result = super(PurchaseOrder, self.with_context(
            is_devolution=self.is_devolution)).action_create_invoice()
        return result
