# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, values):
        res = super(ProductTemplate, self).write(values)
        get_param = self.env['ir.config_parameter'].sudo().get_param
        automatic_update = get_param('sale.automatic_price_update') == 'True'
        if "list_price" in values and automatic_update:
            lines = self.env["sale.order.template.line"].search([
                ("product_id", "in", self.mapped("product_variant_ids").ids),
            ])
            lines.update_price()
            options = self.env["sale.order.template.option"].search([
                ("product_id", "in", self.mapped("product_variant_ids").ids),
            ])
            options.update_price()
        return res
