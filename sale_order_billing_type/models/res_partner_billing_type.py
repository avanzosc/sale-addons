# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartnerBillingType(models.Model):
    _name = "res.partner.billing.type"
    _description = "Partner billing type"
    _order = "name asc"

    name = fields.Char(string="Description", required=True, copy=False)
