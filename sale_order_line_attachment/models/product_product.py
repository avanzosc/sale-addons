from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def button_show_attachments(self):
        self.ensure_one()
        return self.product_tmpl_id.button_show_attachments()
