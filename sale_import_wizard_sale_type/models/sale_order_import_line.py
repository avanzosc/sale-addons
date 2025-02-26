from odoo import models


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    def _sale_order_values(self):
        values = super()._sale_order_values()
        if self.customer_id.sale_type:
            values["type_id"] = self.customer_id.sale_type.id
        return values
