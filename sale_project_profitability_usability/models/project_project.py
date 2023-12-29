# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    out_invoice_amount_total = fields.Monetary(
        string="Total out invoice with tax",
        compute="_compute_total_out_invoice"
    )
    amount_collected = fields.Monetary(
        string="Amount collected",
        compute="_compute_total_out_invoice"
    )
    in_invoice_amount_total = fields.Monetary(
        string="Total in invoice with tax",
        compute="_compute_total_in_invoice"
    )
    amount_paid = fields.Monetary(
        string="Amount paid", compute="_compute_total_in_invoice"
    )

    def _compute_profitability(self):
        for project in self:
            profitability_items = project._get_profitability_items(False)
            costs = profitability_items["costs"]["total"]
            revenues = profitability_items["revenues"]["total"]
            project.revenue_invoiced_amount = revenues["invoiced"]
            project.revenue_to_invoice_amount = revenues["to_invoice"]
            project.cost_invoiced_amount = costs["billed"]
            project.cost_to_invoice_amount = costs["to_bill"]
            project.profitability_done_amount = revenues["invoiced"] + costs["billed"]
            project.profitability_pending_amount = (
                revenues["to_invoice"] + costs["to_bill"]
            )

    def _compute_total_out_invoice(self):
        for project in self:
            action_window = project.action_open_project_invoices()
            out_invoice_amount_total = 0
            amount_collected = 0
            if ("domain" in action_window and
                    action_window.get("domain", False)):
                invoices = self.env["account.move"].search(
                    action_window.get("domain"))
                if invoices:
                    out_invoices = invoices.filtered(
                        lambda x: x.move_type == "out_invoice" and
                        x.state != "cancel")
                    if out_invoices:
                        amount_total = sum(
                            out_invoices.mapped("amount_total"))
                        amount_residual = sum(
                            out_invoices.mapped("amount_residual"))
                        out_invoice_amount_total += amount_total
                        amount_collected += amount_total - amount_residual
                    out_refund_invoices = invoices.filtered(
                        lambda x: x.move_type == "out_refund" and
                        x.state != "cancel")
                    if out_refund_invoices:
                        amount_total = sum(
                            out_refund_invoices.mapped("amount_total"))
                        amount_residual = sum(
                            out_refund_invoices.mapped("amount_residual"))
                        out_invoice_amount_total -= amount_total
                        amount_collected -= amount_total - amount_residual
            project.out_invoice_amount_total = out_invoice_amount_total
            project.amount_collected = amount_collected

    def _compute_total_in_invoice(self):
        for project in self:
            action_window = project.action_open_project_vendor_bills()
            in_invoice_amount_total = 0
            amount_paid = 0
            if ("domain" in action_window and
                    action_window.get("domain", False)):
                invoices = self.env["account.move"].search(
                    action_window.get("domain"))
                if invoices:
                    in_invoices = invoices.filtered(
                        lambda x: x.move_type == "in_invoice" and
                        x.state != "cancel")
                    if in_invoices:
                        amount_total = sum(
                            in_invoices.mapped("amount_total"))
                        amount_residual = sum(
                            in_invoices.mapped("amount_residual"))
                        in_invoice_amount_total += amount_total
                        amount_paid += amount_total - amount_residual
                    in_refund_invoices = invoices.filtered(
                        lambda x: x.move_type == "in_refund" and
                        x.state != "cancel")
                    if in_refund_invoices:
                        amount_total = sum(
                            in_refund_invoices.mapped("amount_total"))
                        amount_residual = sum(
                            in_refund_invoices.mapped("amount_residual"))
                        in_invoice_amount_total -= amount_total
                        amount_paid -= amount_total - amount_residual
            project.in_invoice_amount_total = in_invoice_amount_total
            project.amount_paid = amount_paid
