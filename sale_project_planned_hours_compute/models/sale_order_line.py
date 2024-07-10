from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_project_sale_hourly_rate = fields.Float(
        string="Sale Hourly Rate",
        compute="_compute_order_project_sale_hourly_rate",
        store=False,
    )

    @api.depends("task_id.planned_hours")
    def _compute_order_project_sale_hourly_rate(self):
        temp_sale_hourly_rate = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "sale_project_planned_hours_compute.sale_hourly_rate", default=50
            )
        )

        for line in self:
            line.order_project_sale_hourly_rate = temp_sale_hourly_rate
            if line.order_id.state == "sale" and line.task_id:
                if line.product_uom_qty > 0 and temp_sale_hourly_rate > 0:
                    hours = line.price_subtotal / temp_sale_hourly_rate
                    line.task_id.planned_hours = hours
                else:
                    line.task_id.planned_hours = 0

    @api.onchange(
        "product_uom_qty",
        "price_subtotal",
    )
    def _compute_planned_hours(self):
        temp_sale_hourly_rate = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "sale_project_planned_hours_compute.sale_hourly_rate", default=50
            )
        )

        for line in self:
            if line.order_id.state == "sale" and line.task_id:
                if line.product_uom_qty > 0 and temp_sale_hourly_rate > 0:
                    hours = line.price_subtotal / temp_sale_hourly_rate
                    line.task_id.planned_hours = hours
                else:
                    line.task_id.planned_hours = 0
