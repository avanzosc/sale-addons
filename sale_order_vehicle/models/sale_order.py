# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
    )

    def _prepare_analytic_account_data(self, prefix=None):
        values = super(SaleOrder, self)._prepare_analytic_account_data(prefix=prefix)
        values.update(
            {
                "vehicle_id": self.vehicle_id.id,
            }
        )
        return values


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values.update(
            {
                "vehicle_id": self.order_id.vehicle_id.id,
            }
        )
        return values
