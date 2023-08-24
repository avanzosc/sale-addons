# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    spare_serial_number_id = fields.Many2one(
        string="Spare serial number", comodel_name="stock.production.lot",
        copy=False
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed products", comodel_name="product.product")

    @api.onchange("spare_serial_number_id")
    def onchange_spare_serial_number_id(self):
        for sale in self:
            allowed_product = []
            if sale.spare_serial_number_id:
                bom = sale.search_boms_for_allowed_product_ids()
                if bom and bom.bom_line_ids:
                    allowed_product = bom.bom_line_ids.mapped("product_id")
            sale.allowed_product_ids = (
                [(6, 0, allowed_product.ids)] if allowed_product else
                [(6, 0, [])])
            if sale.spare_serial_number_id:
                sale.order_line.write(
                    {"spare_serial_number_id": sale.spare_serial_number_id})
            else:
                sale.order_line.write(
                    {"spare_serial_number_id": False})

    def search_boms_for_allowed_product_ids(self):
        mrp_bom_obj = self.env["mrp.bom"]
        cond = [("product_id", "!=", False),
                ("product_id", "=", self.spare_serial_number_id.product_id.id)]
        boms = mrp_bom_obj.search(cond)
        if not boms:
            product = self.spare_serial_number_id.product_id
            cond = [("product_tmpl_id", "=", product.product_tmpl_id.id)]
            boms = mrp_bom_obj.search(cond)
        if boms and len(boms) > 1:
            bom = min(boms, key=lambda x: x.sequence)
            return bom
        return boms if boms else False
