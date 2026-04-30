# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CRMTag(models.Model):
    _inherit = "crm.tag"

    is_pre_order = fields.Boolean()
