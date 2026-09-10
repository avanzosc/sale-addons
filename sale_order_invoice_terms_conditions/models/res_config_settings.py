# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    transfering_sale_terms_conditions = fields.Boolean(
        string="Transferring sales order terms and conditions to invoices",
        config_parameter="sale_order_invoice_terms_conditions.transfering_sale_terms_conditions",
    )
