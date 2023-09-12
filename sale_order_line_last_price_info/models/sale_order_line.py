# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        string="Order Date", related="order_id.date_order", store=True, copy=False
    )
    sale_last_price_unit = fields.Float(
        string="LPS",
        digits="Product Price",
        compute="_compute_last_price_unit",
        store=True,
        copy=False,
        precompute=True,
    )
    invoice_last_price_unit = fields.Float(
        string="LPI",
        digits="Product Price",
        compute="_compute_last_price_unit",
        store=True,
        copy=False,
        precompute=True,
    )

    @api.depends("product_id", "order_partner_id")
    def _compute_last_price_unit(self):
        for line in self:
            sale_last_price_unit = 0
            invoice_last_price_unit = 0
            if line.order_partner_id and line.product_id:
                cond = [
                    ("order_partner_id", "=", line.order_partner_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("order_id.state", "not in", ("draft", "cancel")),
                ]
                sl = self.env["sale.order.line"].search(cond, order="date_order desc")
                if sl:
                    sale_last_price_unit = sl[0].price_unit
                cond = [
                    ("partner_id", "=", line.order_partner_id.id),
                    ("move_id", "!=", False),
                    ("product_id", "!=", False),
                    ("product_id", "=", line.product_id.id),
                    ("move_id.state", "not in", ("draft", "cancel")),
                    ("move_id.move_type", "=", "out_invoice"),
                ]
                il = self.env["account.move.line"].search(
                    cond, order="invoice_date desc"
                )
                if il:
                    invoice_last_price_unit = il[0].price_unit
            line.sale_last_price_unit = sale_last_price_unit
            line.invoice_last_price_unit = invoice_last_price_unit
