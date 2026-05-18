from odoo import models
from odoo.tools.float_utils import float_compare


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_virtual_available_website(self, product):
        website = self.env["website"].get_current_website()
        return product.with_context(
            warehouse=website._get_warehouse_available()
        ).virtual_available

    def _get_cart_and_free_qty(self, line=None, product=None, **kwargs):
        cart_qty, free_qty = super()._get_cart_and_free_qty(
            line=line, product=product, **kwargs
        )

        product = product or (line and line.product_id)

        if product and product.product_tmpl_id.use_virtual_stock:
            free_qty = self._get_virtual_available_website(product)

        return cart_qty, free_qty

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        values = super()._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            **kwargs
        )

        line = self.env["sale.order.line"].browse(values.get("line_id"))
        if not line:
            return values

        product = line.product_id

        if product.type != "product" or not product.product_tmpl_id.use_virtual_stock:
            return values

        virtual_qty = self._get_virtual_available_website(product)

        if (
            float_compare(
                line.product_uom_qty,
                virtual_qty,
                precision_rounding=product.uom_id.rounding,
            )
            > 0
        ):
            line.product_uom_qty = max(virtual_qty, 0)

            values.update(
                {
                    "quantity": line.product_uom_qty,
                    "cart_quantity": self.cart_quantity,
                    "warning": (
                        "Solo hay %s unidades disponibles según stock pronosticado."
                    )
                    % virtual_qty,
                }
            )

        return values
