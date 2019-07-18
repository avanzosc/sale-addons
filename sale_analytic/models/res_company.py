# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class company(models.Model):
    _inherit = 'res.company'

    autocreate_sale_analytic_account = fields.Boolean(
        string="Autocreate sale analytic account")
