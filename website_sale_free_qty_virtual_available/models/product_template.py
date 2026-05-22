from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    use_virtual_stock = fields.Boolean(
        string="virtual stock use",
    )

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):
        combination_info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            pricelist=pricelist,
            parent_combination=parent_combination,
            only_template=only_template,
        )

        if not self.env.context.get("website_sale_stock_get_quantity"):
            return combination_info

        if not combination_info.get("product_id"):
            return combination_info

        product = (
            self.env["product.product"].sudo().browse(combination_info["product_id"])
        )

        if product.product_tmpl_id.use_virtual_stock:
            website = self.env["website"].get_current_website()
            virtual_qty = product.with_context(
                warehouse=website._get_warehouse_available()
            ).virtual_available

            combination_info.update(
                {
                    "free_qty": virtual_qty,
                    "virtual_available": virtual_qty,
                    "use_virtual_stock": True,
                    "allow_out_of_stock_order": False,
                }
            )

        return combination_info
