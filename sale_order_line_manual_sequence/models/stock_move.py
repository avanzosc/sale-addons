# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    manual_sequence = fields.Char(
        string='Manual seq.')
