from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # @api.multi
    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1,
        pricelist=False,
        parent_combination=False,
        only_template=False,
    ):

        res = super()._get_combination_info(
            combination,
            product_id,
            add_qty,
            pricelist,
            parent_combination,
            only_template,
        )

        quantity = self.env.context.get("quantity", add_qty)
        context = dict(
            self.env.context,
            quantity=quantity,
            pricelist=pricelist.id if pricelist else False,
        )
        product_template = self.with_context(**context)
        recommended_price = product_template.recommended_price

        res.update({"recommended_price": recommended_price})

        return res
