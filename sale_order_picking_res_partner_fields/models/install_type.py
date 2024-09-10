from odoo import fields, models


class InstallType(models.Model):
    _name = "install.type"
    _description = "Installation Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
