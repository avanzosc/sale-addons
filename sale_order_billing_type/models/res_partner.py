# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    billing_type_id = fields.Many2one(
        string="Billing type", comodel_name="res.partner.billing.type",
        required=True, copy=False
    )
