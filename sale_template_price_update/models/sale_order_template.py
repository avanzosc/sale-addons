# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    @api.multi
    def update_price(self):
        for templ in self:
            templ.sale_order_template_line_ids.update_price()
            templ.sale_order_template_option_ids.update_price()
