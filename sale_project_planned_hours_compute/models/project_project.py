from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    sale_hourly_rate = fields.Float(string="Sale Hourly Rate", default=50)