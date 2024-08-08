# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    sale_import_id = fields.Many2one(
        string="From Sale Import",
        comodel_name="sale.order.import",
        copy=False,
        readonly="1",
    )
