# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    allow_modification_old_offers = fields.Boolean(
        string="Allow Modification Of Old Offers",
        config_parameter="sale_order_offer_version.allow_modification_old_offers",
    )
