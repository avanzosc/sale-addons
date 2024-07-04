import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_project_sale_hourly_rate = fields.Float(
        string="Sale Hourly Rate",
        compute="_compute_order_project_sale_hourly_rate",
        store=False,
    )

    @api.depends("task_id.planned_hours")
    def _compute_order_project_sale_hourly_rate(self):
        _logger.info("Starting _compute_order_project_sale_hourly_rate")
        temp_sale_hourly_rate = float(
            self.env["res.config.settings"].sudo().search([], limit=1).sale_hourly_rate
        )
        _logger.info(f"Retrieved sale hourly rate: {temp_sale_hourly_rate}")

        for line in self:
            line.order_project_sale_hourly_rate = temp_sale_hourly_rate
            _logger.info(f"Set order_project_sale_hourly_rate: {temp_sale_hourly_rate} for line {line.id}")
            if line.order_id.state == "sale" and line.task_id:
                _logger.info(f"Order is in 'sale' state and task_id is present for line {line.id}")
                if line.product_uom_qty > 0 and temp_sale_hourly_rate > 0:
                    hours = line.price_subtotal / temp_sale_hourly_rate
                    _logger.info(f"Computed planned hours: {hours} for line {line.id}")

                    line.task_id.planned_hours = hours
                else:
                    _logger.info(f"Set planned hours to 0 for line {line.id}")
                    line.task_id.planned_hours = 0

    @api.onchange(
        "product_uom_qty",
        "price_subtotal",
    )
    def _compute_planned_hours(self):
        _logger.info("Starting _compute_planned_hours")
        temp_sale_hourly_rate = float(
            self.env["res.config.settings"].sudo().search([], limit=1).sale_hourly_rate
        )
        _logger.info(f"Retrieved sale hourly rate: {temp_sale_hourly_rate}")

        for line in self:
            _logger.info(f"Processing line {line.id}")
            if line.order_id.state == "sale" and line.task_id:
                _logger.info(f"Order is in 'sale' state and task_id is present for line {line.id}")
                if line.product_uom_qty > 0 and temp_sale_hourly_rate > 0:
                    hours = line.price_subtotal / temp_sale_hourly_rate
                    _logger.info(f"Computed planned hours: {hours} for line {line.id}")

                    line.task_id.planned_hours = hours
                else:
                    _logger.info(f"Set planned hours to 0 for line {line.id}")
                    line.task_id.planned_hours = 0
