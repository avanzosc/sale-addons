# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ShopifyPaymentGatewayEpt(models.Model):
    _inherit = "shopify.payment.gateway.ept"

    journal_id = fields.Many2one(comodel_name="account.journal")
