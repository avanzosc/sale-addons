# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    final_customer = fields.Boolean(
        string="Final customer",
        default=False,
        help="Marks delivery addresses that correspond to the final customer.",
    )
