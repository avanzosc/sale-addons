# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    return_journal_id = fields.Many2one(
        string="Return Journal",
        comodel_name="account.journal",
        domain=[("type", "=", "sale")]
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    return_journal_id = fields.Many2one(
        string="Return Journal",
        comodel_name="account.journal",
        domain=[("type", "=", "sale")],
        related='company_id.return_journal_id',
        readonly=False
    )
