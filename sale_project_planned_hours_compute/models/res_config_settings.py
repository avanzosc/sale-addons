from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_hourly_rate = fields.Float(
        string="Sale Hourly Rate",
        default=50,
        config_parameter="sale_project_planned_hours_compute.sale_hourly_rate",
    )
