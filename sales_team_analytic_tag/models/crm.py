# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag', relation='rel_analytic_tags',
        column1='crm_team_id', column2='analytic_tag_id',
        string='Analytic tags')
