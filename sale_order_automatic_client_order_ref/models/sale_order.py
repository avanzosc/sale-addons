# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    internal_order_reference = fields.Char(copy=False)
    customer_order_code = fields.Char(copy=False)
    client_project_name = fields.Char(copy=False)
    assigned_technician_id = fields.Many2one(comodel_name="hr.employee")
    client_order_ref = fields.Char(
        compute="_compute_client_order_ref",
        store=True,
        readonly=True,
        copy=False,
    )

    @api.depends(
        "internal_order_reference", "customer_order_code", "client_project_name"
    )
    def _compute_client_order_ref(self):
        for order in self:
            values = [
                order.internal_order_reference,
                order.customer_order_code,
                order.client_project_name,
            ]
            order.client_order_ref = "/".join(value for value in values if value)
