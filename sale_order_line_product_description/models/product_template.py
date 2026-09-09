# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    no_product_description_to_sale_invoice_lines = fields.Boolean(
        string="Do Not Add product descriptions to sales and invoice lines",
        default=False,
    )
