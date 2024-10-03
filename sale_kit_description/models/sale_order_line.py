from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _set_bom_description(self):
        """Helper method to set the description based on BOM."""
        if self.product_id and self.product_id.bom_ids:
            bom = self.env["mrp.bom"].search(
                [
                    ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                    ("active", "=", True),
                ],
                order="sequence",
                limit=1,
            )

            if bom:
                description_lines = [self.product_id.name]
                description_lines += [
                    f"- {line.product_id.name} {line.product_qty} {line.product_uom_id.name}"
                    for line in bom.bom_line_ids
                ]
                self.name = "\n".join(description_lines)

    @api.onchange("product_id")
    def _onchange_sale_description_product_id(self):
        """Onchange method to update description when product is changed."""
        self._set_bom_description()

    @api.model
    def create(self, vals):
        """Override create method to set the description for new sale order lines."""
        sale_order_line = super().create(vals)
        if "product_id" in vals:
            product_id = self.env["product.product"].browse(vals["product_id"])
            if product_id and product_id.bom_ids:
                sale_order_line._set_bom_description()
        return sale_order_line
