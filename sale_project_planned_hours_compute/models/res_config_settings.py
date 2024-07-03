from odoo import api, models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_hourly_rate = fields.Float(string="Sale Hourly Rate", default=50)

