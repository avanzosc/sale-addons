# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_industry_id = fields.Many2one(
        string="Industry",
        comodel_name="res.partner.industry",
        related="partner_id.industry_id",
        readonly=True,
        store=True,
        copy=False,
    )
    customer_principal_activity_id = fields.Many2one(
        string="Customer Principal Activity",
        comodel_name="principal.activity",
        related="partner_id.principal_activity_id",
        store=True,
        readonly=True,
    )
