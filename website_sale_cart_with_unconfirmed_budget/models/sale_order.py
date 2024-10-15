from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        unconfirmed_budget = self.env["sale.order"].search(
            [
                ("state", "=", "draft"),
                ("partner_id", "=", vals.get("partner_id")),
            ],
            limit=1,
        )

        if unconfirmed_budget:
            unconfirmed_budget.order_line.unlink()
            for line in vals.get("order_line", []):
                unconfirmed_budget.order_line.create(
                    {
                        "order_id": unconfirmed_budget.id,
                        "product_id": line[2]["product_id"],
                        "product_uom_qty": line[2]["product_uom_qty"],
                    }
                )
            return unconfirmed_budget

        return super().create(vals)
