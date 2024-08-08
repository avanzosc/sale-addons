from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_basket = fields.Boolean(
        "Is a Basket",
    )
