# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    producer = fields.Char()
    product_link = fields.Char()

    @api.onchange("product_id")
    def _onchange_product_id_producer_link(self):
        self.producer = self.product_id.description_sale or False
        self.product_link = self.product_id.external_url or False
