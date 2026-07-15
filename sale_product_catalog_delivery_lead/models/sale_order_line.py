# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "order_id.catalog_id")
    def _compute_customer_lead(self):
        """Take the delivery lead time from the order catalog when set.

        ``super()`` keeps the standard behaviour (the product's customer lead
        time). When the order catalog defines a delivery lead time greater
        than 0, it overrides the product value. The dependency is on
        ``order_id.catalog_id`` (a plain stored field) so ``customer_lead``
        stays precomputable at line creation, and assigning or changing the
        catalog on the order header recomputes every line.
        """
        res = super()._compute_customer_lead()
        for line in self:
            catalog = line.order_id.catalog_id
            if catalog and catalog.delivery_lead_days > 0:
                line.customer_lead = catalog.delivery_lead_days
        return res
