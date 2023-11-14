# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleCommissionSettlement(models.Model):
    _inherit = "sale.commission.settlement"

    def _get_comissions_to_print(self, invoice):
        commissions = self.line_ids.filtered(
            lambda x: x.invoice_id == invoice).mapped(
                "commission_id").sorted(key=lambda l: (l.name))
        lines_to_print = []
        for commission in commissions:
            lines= self.line_ids.filtered(
                lambda x: x.invoice_id == invoice and
                    x.commission_id == commission)
            vals = {
                "invoice_date": invoice.date,
                "invoice_name": invoice.name,
                "invoice_customer": invoice.partner_id.name,
                "invoice_shipping_address": invoice.partner_shipping_id.name,
                "invoice_amount_untaxed": invoice.amount_untaxed,
                "commission_name": commission.name,
            }
            settled_amount = 0
            commissionable_tax_base = 0
            for line in lines:
                if line.settled_amount:
                    commissionable_tax_base += (
                        line.invoice_line_id.price_subtotal)
                    settled_amount += line.settled_amount
            vals.update({
                "invoice_commissionable_tax_base": commissionable_tax_base,
                "settled_amount": settled_amount
                })
            lines_to_print.append(vals)
        return lines_to_print
