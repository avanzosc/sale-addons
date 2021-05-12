# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    is_member = fields.Boolean(string='Is member?', default=False)
