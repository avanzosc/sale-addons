#   Copyright 2023 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    control_unique_client_order_ref = fields.Boolean(
        string="Unique ref/description control?", default=True, copy=False
    )

    @api.model
    def create(self, vals):
        if "client_order_ref" in vals and vals.get("client_order_ref", False):
            cond = [("client_order_ref", "=", vals.get("client_order_ref"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if (
                sale
                and "control_unique_client_order_ref" in vals
                and vals.get("control_unique_client_order_ref", False)
            ):
                error = _(
                    "The sales order %(order_ref)s already exists, with customer"
                    " reference: %(customer_ref)s"
                ) % {
                    "order_ref": sale.name,
                    "customer_ref": sale.client_order_ref,
                }
                raise ValidationError(error)
        return super().create(vals)
