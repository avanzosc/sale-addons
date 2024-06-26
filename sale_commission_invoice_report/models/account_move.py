# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    commissionable_tax_base = fields.Monetary(
        string="Commissionable tax base",
        compute="_compute_commissionable_tax_base_and_percentage",
        store=True,
        copy=False,
    )
    percentage_average_commission = fields.Float(
        string="% Average commission",
        compute="_compute_commissionable_tax_base_and_percentage",
        store=False,
        copy=False,
    )

    @api.depends("line_ids.price_subtotal", "commission_total")
    def _compute_commissionable_tax_base_and_percentage(self):
        for invoice in self:
            commissionable_tax_base = 0.0
            percentage_average_commission = 0.0
            for line in invoice.line_ids:
                commission_total = sum(x.amount for x in line.agent_ids)
                if commission_total != 0:
                    commissionable_tax_base += line.price_subtotal
            if commissionable_tax_base and invoice.commission_total:
                percentage_average_commission = (
                    invoice.commission_total / commissionable_tax_base
                )
            invoice.commissionable_tax_base = commissionable_tax_base
            invoice.percentage_average_commission = percentage_average_commission * 100
