# Copyright 2026 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    old_account_analytic_account_id = fields.Many2one(
        string="Analytic Account Not Migrated", comodel_name="account.analytic.account"
    )
