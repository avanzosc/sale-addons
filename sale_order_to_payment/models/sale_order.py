# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_ids = fields.Many2many(
        string="Payments",
        comodel_name="account.payment",
        compute="_compute_payment_ids")
    payment_count = fields.Integer(
        string="Payments Count",
        compute="_compute_payment_count")

    def _compute_payment_count(self):
        for sale in self:
            sale.payment_count = len(sale.payment_ids)

    def _compute_payment_ids(self):
        for sale in self:
            sale.payment_ids = False
            payments = []
            for move in sale.invoice_ids:
                for payment in move.payment_ids:
                    if payment not in payments:
                        payments.append(payment.id)
            if payments:
                sale.payment_ids = [(6, 0, payments)]

    def action_view_payments(self):
        return {
            "name": _("Payments"),
            "view_mode": "tree,form",
            "res_model": "account.payment",
            "domain": [("id", "in", self.payment_ids.ids)],
            "type": "ir.actions.act_window",
            "context": self.env.context
            }