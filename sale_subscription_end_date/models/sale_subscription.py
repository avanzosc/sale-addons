# Copyright (c) 2022 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models
from dateutil.relativedelta import relativedelta


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    @api.onchange('date_start', 'template_id')
    def onchange_date_start(self):
        result = super(SaleSubscription, self).onchange_date_start()
        if self.date:
            end_date = self.date + relativedelta(days=-1)
            self.date = end_date
        return result
