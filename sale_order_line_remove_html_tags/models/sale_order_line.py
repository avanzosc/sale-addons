# Copyright 2021 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
import re


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def get_sale_order_line_multiline_description_sale(self, product):
        res = super().get_sale_order_line_multiline_description_sale(product)
        html_tags = re.compile(r'<[^>]+>')
        return html_tags.sub('', res)
