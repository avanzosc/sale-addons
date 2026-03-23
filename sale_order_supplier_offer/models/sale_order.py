# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    supplier_offer_number = fields.Char(string="Supplier offer number", copy=False)
    supplier_offer_file = fields.Many2one(
        string="Supplier offer file", comodel_name="ir.attachment", copy=False
    )
