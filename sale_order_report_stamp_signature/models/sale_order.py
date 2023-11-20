# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_stamp_signature = fields.Boolean(
        string="Print stamp and signature", default=True)
