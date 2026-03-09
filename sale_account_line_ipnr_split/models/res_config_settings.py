# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_ipnr_product_id = fields.Many2one(
        comodel_name="product.product",
        string="IPNR Product",
        config_parameter="ipnr.product_id",
        domain="[('default_code', '!=', False)]",
        help="Product used to represent the IPNR line in sales orders and invoices.",
    )
    x_ipnr_rounding_digits = fields.Integer(
        string="Rounding decimals",
        config_parameter="ipnr.rounding_digits",
        default=6,
        help="Number of decimal places used when rounding IPNR unit prices (default: 6).",
    )
