from odoo import http
from odoo.http import request

from odoo.addons.sale.controllers.variant import VariantController


class VariantControllerInherit(VariantController):

    @http.route(
        ["/sale/get_combination_info"], type="json", auth="user", methods=["POST"]
    )
    def get_combination_info(
        self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw
    ):
        combination = super().get_combination_info(
            product_template_id, product_id, combination, add_qty, pricelist_id, **kw
        )

        # Retrieve the product.template and add the virtual_available field to combination
        product_template = request.env["product.template"].browse(
            int(product_template_id)
        )
        combination.update({"virtual_available": product_template.virtual_available})

        return combination
