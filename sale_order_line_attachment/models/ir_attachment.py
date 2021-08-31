# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    attach_in_sales_orders = fields.Boolean(
        string='Attach in sales orders', default=True)
