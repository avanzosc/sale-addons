# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    no_upadate_returns = fields.Boolean(default=False)

    def _search_pending_negative_line(self, move):
        return self.env["sale.order.line"].search(
            [
                ("order_partner_id", "=", move.picking_id.partner_id.id),
                ("state", "=", "sale"),
                ("product_id", "=", move.product_id.id),
                ("pending_qty", "<", 0),
                ("price_unit", "=", 0),
            ],
            limit=1,
        )

    def _process_incoming_move(self, move):
        if not move.purchase_line_id or not move.purchase_line_id.sale_order_line_ids:
            return

        qty = move.quantity
        sales = move.purchase_line_id.sale_order_line_ids.sorted("create_date")
        sale_line_ids = []
        index = 0

        while qty > 0 and index < len(sales):
            sale = sales[index]
            sale_line_ids.append(sale.id)
            pending = sale.pending_qty
            returned = sale.returned_amount
            if qty <= pending:
                returned += qty
                pending -= qty
                qty = 0
            else:
                returned += pending
                qty -= pending
                pending = 0
            sale.write({"returned_amount": returned, "pending_qty": pending})
            index += 1

        if qty > 0:
            pending_negative = self._search_pending_negative_line(move)
            if not pending_negative:
                pending_negative = sales[index - 1]
            pending_negative.pending_qty -= qty
            pending_negative.returned_amount += qty

        move.purchase_line_id.sale_order_line_ids = [(6, 0, sale_line_ids)]

    def _process_outgoing_move(self, move):
        qty = move.quantity
        while qty > 0:
            pending_negative = self._search_pending_negative_line(move)
            if pending_negative and abs(pending_negative.pending_qty) >= qty:
                pending_negative.pending_qty += qty
                qty = 0
            elif pending_negative:
                qty += pending_negative.pending_qty
                pending_negative.pending_qty = 0
            else:
                move.sale_line_id.pending_qty = qty
                qty = 0

    def _post_validate_updates(self):
        for picking in self:
            if picking.picking_type_code == "incoming":
                if picking.no_upadate_returns:
                    picking.no_upadate_returns = False
                    continue
                for move in picking.move_ids_without_package.filtered(
                    lambda record: record.product_id.returnable
                ):
                    picking._process_incoming_move(move)
                picking.no_upadate_returns = True
            elif picking.picking_type_code == "outgoing":
                for move in picking.move_ids_without_package.filtered(
                    lambda record: record.product_id.returnable
                ):
                    picking._process_outgoing_move(move)

    def button_validate(self):
        for picking in self:
            lines = picking.move_line_ids_without_package.filtered(
                lambda record: record.quantity != 0
            )
            if not lines:
                picking.button_force_done_detailed_operations()

        result = super().button_validate()
        self._post_validate_updates()
        return result
