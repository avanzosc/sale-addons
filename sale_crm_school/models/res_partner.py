# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def create_enrollment(self, next_year, center, course, group=False):
        self.ensure_one()
        current_group = self.get_current_group()
        if current_group.center_id == center:
            return super(ResPartner, self).create_enrollment(
                next_year, center, course, group=group)
        self.env["crm.lead"].find_or_create_enrollment(
            self, next_year, center, course)
        return True
