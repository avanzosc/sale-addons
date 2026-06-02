# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_ids = fields.Many2many(
        string="Payments",
        comodel_name="account.payment",
        compute="_compute_payment_ids",
    )
    payment_count = fields.Integer(
        string="Payments Count", compute="_compute_payment_count"
    )

    @api.depends("payment_ids")
    def _compute_payment_count(self):
        for sale in self:
            sale.payment_count = len(sale.payment_ids)

    @api.depends("invoice_ids.reconciled_payment_ids")
    def _compute_payment_ids(self):
        for sale in self:
            payments = self.env["account.payment"]
            for move in sale.invoice_ids:
                payments |= move.reconciled_payment_ids
            sale.payment_ids = payments

    def action_view_payments(self):
        self.ensure_one()
        context = self.env.context.copy()
        if self.partner_id:
            context.update({"default_partner_id": self.partner_id.id})
        return {
            "name": _("Payments"),
            "view_mode": "list,form",
            "res_model": "account.payment",
            "domain": [("id", "in", self.payment_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
