# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        product_ids = super()._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
        if name and self._context.get("partner_id"):
            cond = [
                ("partner_id", "=", self._context.get("partner_id")),
                ("customer_code", operator, name),
            ]
            product_codes = self.env["product.template.customer.code"].search(cond)
            for product_code in product_codes:
                for product in product_code.template_id.product_variant_ids:
                    product_ids.append(product.id)
        return product_ids
