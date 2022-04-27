# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange("partner_invoice_id")
    def onchange_partner_invoice_id(self):
        for sale in self:
            if (sale.partner_id and sale.partner_invoice_id and
                sale.partner_id != sale.partner_invoice_id and
                    sale.partner_invoice_id.property_payment_term_id):
                sale.payment_term_id = (
                    sale.partner_invoice_id.property_payment_term_id.id)

    @api.depends("partner_id", "partner_invoice_id")
    def _compute_payment_mode(self):
        result = super(SaleOrder, self)._compute_payment_mode()
        for sale in self:
            if (sale.partner_id and sale.partner_invoice_id and
                sale.partner_id != sale.partner_invoice_id and
                    sale.partner_invoice_id.customer_payment_mode_id):
                sale.payment_mode_id = (
                    sale.partner_invoice_id.customer_payment_mode_id.id)
        return result
