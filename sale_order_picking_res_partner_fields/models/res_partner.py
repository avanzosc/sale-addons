from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_timetable = fields.Char(
        string="Delivery Timetable",
    )
