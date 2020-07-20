# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    autocreate_sale_analytic_account = fields.Boolean(
        related='company_id.autocreate_sale_analytic_account',
        string="Auto Analytic account", readonly=False)
