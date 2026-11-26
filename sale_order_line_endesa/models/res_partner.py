# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_endesa = fields.Boolean(
        help="Sale orders of this customer are delivered through the Endesa "
        "platform. Set it on the company: its contacts follow it.",
    )
