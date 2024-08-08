from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def _onchange_sale_description_product_id(self):

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
                self.name = self.product_id.name

                bom_lines = bom.bom_line_ids

                description_lines = [self.name]
                for line in bom_lines:
                    description_line = f"""- {line.product_id.name} \
{line.product_qty} {line.product_uom_id.name}"""
                    description_lines.append(description_line)

                self.name = "\n".join(description_lines)
