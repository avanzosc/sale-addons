from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_project_sale_hourly_rate = fields.Float(
        string="Sale Hourly Rate",
        compute="_compute_order_project_sale_hourly_rate",
        store=False,
    )

    @api.depends("order_id.project_id.sale_hourly_rate")
    def _compute_order_project_sale_hourly_rate(self):
        for line in self:
            line.order_project_sale_hourly_rate = (
                line.order_id.project_id.sale_hourly_rate
            )
            if (
                line.order_id.state == "sale"
                and line.order_id.project_id
                and line.task_id
            ):
                if (
                    line.product_uom_qty > 0
                    and line.order_id.project_id.sale_hourly_rate
                ):
                    hours = line.price_subtotal / (
                        line.product_uom_qty * line.order_id.project_id.sale_hourly_rate
                    )
                    line.task_id.planned_hours = hours
                else:
                    line.task_id.planned_hours = 0

    @api.onchange(
        "product_uom_qty",
        "price_subtotal",
    )
    def _compute_planned_hours(self):
        for line in self:
            if (
                line.order_id.state == "sale"
                and line.order_id.project_id
                and line.task_id
            ):
                if (
                    line.product_uom_qty > 0
                    and line.order_id.project_id.sale_hourly_rate
                ):
                    hours = line.price_subtotal / (
                        line.product_uom_qty * line.order_id.project_id.sale_hourly_rate
                    )
                    line.task_id.planned_hours = hours
                else:
                    line.task_id.planned_hours = 0
