# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    description = fields.Char()
