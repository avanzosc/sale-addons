# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    @api.multi
    def update_price(self):
        for line in self:
            line.price_unit = line.product_id.lst_price
