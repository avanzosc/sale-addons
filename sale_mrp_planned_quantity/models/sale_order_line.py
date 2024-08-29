# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "product_uom_qty",
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
    )
    def _compute_planned_quantity(self):
        super(SaleOrderLine, self)._compute_planned_quantity()
        for order_line in self:
            planned_quantity = order_line.planned_quantity
            if order_line.qty_delivered_method == "stock_move":
                boms = order_line.move_ids.filtered(
                    lambda m: m.state != "cancel"
                ).mapped("bom_line_id.bom_id")
                dropship = any(m._is_dropshipped() for m in order_line.move_ids)
                if not boms and dropship:
                    boms = boms._bom_find(
                        product=order_line.product_id,
                        company_id=order_line.company_id.id,
                        bom_type="phantom",
                    )
                # We fetch the BoMs of type kits linked to the order_line,
                # the we keep only the one related to the finished produst.
                # This bom shoud be the only one since bom_line_id was written on the
                # moves
                relevant_bom = boms.filtered(
                    lambda b: b.type == "phantom"
                    and (
                        b.product_id == order_line.product_id
                        or (
                            b.product_tmpl_id == order_line.product_id.product_tmpl_id
                            and not b.product_id
                        )
                    )
                )
                if relevant_bom:
                    # In case of dropship, we use a 'all or nothing' policy since
                    # 'bom_line_id' was not written on a move coming from a PO: all
                    # moves (to customer) must be done and the returns must be delivered
                    # back to the customer
                    # FIXME: if the components of a kit have different suppliers, multiple
                    # PO are generated. If one PO is confirmed and all the others are in
                    # draft, receiving the products for this PO will set the qty_delivered.
                    # We might need to check the state of all PO as well... but sale_mrp
                    # doesn't depend on purchase.
                    if dropship:
                        moves = order_line.move_ids.filtered(
                            lambda m: m.state != "cancel"
                        )
                        if (
                            any(
                                (
                                    m.location_dest_id.usage == "customer"
                                    and m.state != "done"
                                )
                                or (
                                    m.location_dest_id.usage != "customer"
                                    and m.state == "done"
                                    and float_compare(
                                        m.quantity_done,
                                        sum(
                                            sub_m.product_uom._compute_quantity(
                                                sub_m.quantity_done, m.product_uom
                                            )
                                            for sub_m in m.returned_move_ids
                                            if sub_m.state == "done"
                                        ),
                                        precision_rounding=m.product_uom.rounding,
                                    )
                                    > 0
                                )
                                for m in moves
                            )
                            or not moves
                        ):
                            order_line.planned_quantity = 0
                        else:
                            order_line.planned_quantity = order_line.product_uom_qty
                        continue
                    moves = order_line.move_ids.filtered(
                        lambda m: m.state != "cancel" and not m.scrapped
                    )
                    filters = {
                        "incoming_moves": lambda m: m.location_dest_id.usage
                        == "customer"
                        and (
                            not m.origin_returned_move_id
                            or (m.origin_returned_move_id and m.to_refund)
                        ),
                        "outgoing_moves": lambda m: m.location_dest_id.usage
                        != "customer"
                        and m.to_refund,
                    }
                    order_qty = order_line.product_uom._compute_quantity(
                        order_line.product_uom_qty, relevant_bom.product_uom_id
                    )
                    qty_planned = moves._compute_kit_planned_quantities(
                        order_line.product_id, order_qty, relevant_bom, filters
                    )
                    planned_quantity = relevant_bom.product_uom_id._compute_quantity(
                        qty_planned, order_line.product_uom
                    )

                # If no relevant BOM is found, fall back on the all-or-nothing policy.
                # This happens when the product sold is made only of kits. In this case,
                # the BOM of the stock moves do not correspond to the product sold =>
                # no relevant BOM.
                # elif boms:
                #     # if the move is ingoing, the product **sold** has delivered qty 0
                #     if all(
                #         m.state != "cancel" and m.location_dest_id.usage == "customer"
                #         for m in order_line.move_ids
                #     ):
                #         planned_quantity = order_line.product_uom_qty
                #     else:
                #         planned_quantity = 0.0
            order_line.update(
                {
                    "planned_quantity": planned_quantity,
                    "difference_between_ordered_planned": bool(
                        order_line.product_uom_qty != planned_quantity
                    ),
                }
            )
