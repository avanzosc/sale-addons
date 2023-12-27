# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, values):
        if "is_devolution" in self.env.context and self.env.context["is_devolution"] is True:
            values.update({
                "move_type": "out_refund",
                "journal_id": self.env.company.return_journal_id.id})
        return super(AccountMove, self).create(values)
