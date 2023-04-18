# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    user_id = fields.Many2one(
        string="Commercial",
        comodel_name="res.users")
