# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def write(self, values):
        res = super(ProductProduct, self).write(values)
        get_param = self.env['ir.config_parameter'].sudo().get_param
        automatic_update = get_param('sale.automatic_price_update') == 'True'
        if "lst_price" in values and automatic_update:
            lines = self.env["sale.order.template.line"].search([
                ("product_id", "in", self.ids),
            ])
            lines.update_price()
            options = self.env["sale.order.template.option"].search([
                ("product_id", "in", self.ids),
            ])
            options.update_price()
        return res
