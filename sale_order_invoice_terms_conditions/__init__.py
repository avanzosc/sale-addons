from . import models
from odoo import api, SUPERUSER_ID


def _post_install_sale_order_invoice_terms_conditions(env):
    env["ir.config_parameter"].sudo().set_param(
        "sale_order_invoice_terms_conditions.transfering_sale_terms_conditions",
        True,
    )
