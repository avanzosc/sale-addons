# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=False)
    supplier_offer_number = fields.Char(
        string="Supplier offer number", copy=False, store=True,
        related="sale_order_id.supplier_offer_number"
    )
    supplier_offer_file = fields.Many2one(
        string="Supplier offer file", copy=False, store=True,
        comodel_name="ir.attachment",
        related="sale_order_id.supplier_offer_file"
    )

    @api.model
    def create(self, values):
        purchase = super(PurchaseOrder, self).create(values)
        if "origin" in values and values.get("origin", False):
            cond = [("name", "=", values.get("origin"))]
            sale = self.env["sale.order"].search(cond, limit=1)
            if sale:
                purchase.sale_order_id = sale.id
        return purchase
