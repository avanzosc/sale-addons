from odoo import fields, models


class StructureType(models.Model):
    _name = "structure.type"
    _description = "Structure Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
