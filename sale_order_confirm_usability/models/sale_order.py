# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_done = fields.Float(
        string="Payment Done",
        compute="_compute_payment_done")
    pending_payment = fields.Float(
        string="Pending Payment",
        compute="_compute_pending_payment",
        store=True)
    picking_done = fields.Boolean(
        string="Pickings are done",
        compute="_compute_picking_done",
        store=True)

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_picking_done(self):
        for sale in self:
            sale.picking_done = False
            if (
                sale.picking_ids) and any(
                    [picking.state == "done" for picking in sale.picking_ids]):
                sale.picking_done = True

    @api.depends("invoice_ids", "invoice_ids.amount_total",
                 "invoice_ids.amount_residual")
    def _compute_payment_done(self):
        for sale in self:
            sale.payment_done = 0
            if sale.invoice_ids:
                total = sum(sale.invoice_ids.mapped("amount_total"))
                pendig = sum(sale.invoice_ids.mapped("amount_residual"))
                sale.payment_done = total - pendig

    @api.depends("invoice_ids", "invoice_ids.amount_residual")
    def _compute_pending_payment(self):
        for sale in self:
            sale.pending_payment = 0
            if sale.invoice_ids:
                sale.pending_payment = sum(
                    sale.invoice_ids.mapped("amount_residual"))

    def button_confirm_pickings(self):
        self.ensure_one()
        self.action_confirm()
        for line in self.order_line:
            if line.product_id and (
                line.product_id.tracking != "none") and not (
                    line.lot_id) and line.product_uom_qty:
                raise ValidationError(
                    _("The product {} has not lot").format(
                        line.product_id.name))
        for picking in self.picking_ids:
            picking.button_force_done_detailed_operations()
            for line in picking.move_line_ids_without_package:
                if line.product_id:
                    line.lot_id = line.move_id.sale_line_id.lot_id.id
                    line.qty_done = line.move_id.sale_line_id.product_uom_qty
            res = picking.button_validate()
            return res

    def button_create_invoice_and_paid(self):
        self.ensure_one()
        if not self.invoice_ids:
            self._create_invoices()
        for invoice in self.invoice_ids:
            if invoice.state == "draft":
                invoice.action_post()
            result = invoice.action_register_payment()
            return result
