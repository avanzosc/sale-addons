# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("is_devolution"):
            for vals in vals_list:
                vals.update(
                    {
                        "move_type": "out_refund",
                        "journal_id": self.env.company.return_journal_id.id,
                    }
                )
        return super().create(vals_list)
