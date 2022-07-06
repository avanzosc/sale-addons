# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseRequisitionType(models.Model):
    _inherit = "purchase.requisition.type"
    _name = "sale.requisition.type"
    _description = "Sale Requisition Type"
    _order = "sequence"

    exclusive = fields.Selection(
        help="""
        Select only one RFQ (exclusive):  when a sale order is confirmed, cancel the 
        remaining sale order.\n
        Select multiple RFQ: allows multiple sale orders. On confirmation of a sale 
        order it does not cancel the remaining orders""")


class SaleRequisition(models.Model):
    _inherit = "purchase.requisition"
    _name = "sale.requisition"
    _description = "Sale Requisition"
    _order = "id desc"

    def _get_type_id(self):
        return self.env["sale.requisition.type"].search([], limit=1)

    type_id = fields.Many2one(
        comodel_name="sale.requisition.type",
        string="Agreement Type",
        required=True,
        default=_get_type_id,
    )
    line_ids = fields.One2many(
        comodel_name="sale.requisition.line",
        inverse_name="requisition_id",
        string="Products to Sale",
        states={"done": [("readonly", True)]},
        copy=True,
    )
    sale_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="requisition_id",
        string="Sale Orders",
        states={"done": [("readonly", True)]})

    @api.depends("sale_ids")
    def _compute_orders_number(self):
        for requisition in self:
            requisition.order_count = len(requisition.sale_ids)

    def action_cancel(self):
        # try to set all associated quotations to cancel state
        for requisition in self:
            requisition.sale_ids.button_cancel()
            for po in requisition.sale_ids:
                po.message_post(
                    body=_("Cancelled by the agreement associated to this quotation."))
        self.write({"state": "cancel"})

    def action_in_progress(self):
        self.ensure_one()
        if not all(obj.line_ids for obj in self):
            raise UserError(
                _("You cannot confirm agreement '%s' because there is no product line.") % self.name)
        if self.type_id.quantity_copy == "none" and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(
                        _("You cannot confirm the blanket order without price."))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(
                        _("You cannot confirm the blanket order without quantity."))
            self.write({"state": "ongoing"})
        else:
            self.write({"state": "in_progress"})
        # Set the sequence number regarding the requisition type
        if self.name == "New":
            if self.is_quantity_copy != "none":
                self.name = self.env["ir.sequence"].next_by_code(
                    "sale.requisition.sale.tender")
            else:
                self.name = self.env["ir.sequence"].next_by_code(
                    "sale.requisition.blanket.order")


class SaleRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"
    _name = "sale.requisition.line"
    _description = "Sale Requisition Line"
    _rec_name = "product_id"

    requisition_id = fields.Many2one(
        comodel_name="sale.requisition",
        required=True,
        string="Sale Agreement",
        ondelete="cascade",
    )

    def create_supplier_info(self):
        return True

    @api.depends("requisition_id.sale_ids.state")
    def _compute_ordered_qty(self):
        line_found = set()
        for line in self:
            total = 0.0
            for so in line.requisition_id.sale_ids.filtered(
                    lambda sale_order: sale_order.state in ["sale", "done"]):
                for so_line in so.order_line.filtered(
                        lambda order_line: order_line.product_id == line.product_id):
                    if so_line.product_uom != line.product_uom_id:
                        total += so_line.product_uom._compute_quantity(
                            so_line.product_uom_qty, line.product_uom_id)
                    else:
                        total += so_line.product_uom_qty
            if line.product_id not in line_found :
                line.qty_ordered = total
                line_found.add(line.product_id)
            else:
                line.qty_ordered = 0

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            self.product_qty = 1.0
        if not self.schedule_date:
            self.schedule_date = self.requisition_id.schedule_date

    def _prepare_sale_order_line(
            self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        self.ensure_one()
        return {
            "name": name,
            "product_id": self.product_id.id,
            "product_uom": self.product_id.uom_id.id,
            "product_uom_qty": product_qty,
            "price_unit": price_unit,
            "tax_id": [(6, 0, taxes_ids)],
        }
