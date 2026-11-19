# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_invoice_id = fields.Many2one(
        domain="['|', ('id', '=', partner_id), ('type','=','invoice'),"
        "('parent_id','child_of',partner_id), '|', ('company_id', '=', False),"
        "('company_id', '=', company_id)]"
    )
    partner_shipping_id = fields.Many2one(
        domain="['|', ('id', '=', partner_id), ('type','=','delivery'),"
        "('parent_id','child_of',partner_id), '|', ('company_id', '=', False),"
        "('company_id', '=', company_id)]"
    )
