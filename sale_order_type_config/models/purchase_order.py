# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one(default=False)

    @api.onchange('company_id')
    def _onchange_company_id(self):
        super(PurchaseOrder, self)._onchange_company_id()
        if self.picking_type_id:
            self.picking_type_id = False
