from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_order_not_grouping = fields.Boolean(
        string="Service Order Not Grouping",
        help="Enable to control purchase generation behavior for services in different orders.",
    )
