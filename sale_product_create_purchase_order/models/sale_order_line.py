# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_supplier_ids = fields.Many2many(
        string="Product suppliers",
        comodel_name="product.supplierinfo",
        compute="_compute_product_supplier_ids",
    )
    product_supplier_id = fields.Many2one(
        string="Product Supplier",
        comodel_name="product.supplierinfo",
        compute="_compute_product_supplier_id",
        store=True,
        readonly=False,
        precompute=True,
        copy=False,
    )
    supplier_id = fields.Many2one(
        string="Supplier",
        related="product_supplier_id.partner_id",
        store=True,
        copy=False,
    )
    detailed_type = fields.Selection(
        string="Product Type",
        related="product_id.detailed_type",
    )
    ref_catalogue = fields.Char(
        string="Ref. Catalogue",
        copy=False,
    )
    purchase_line_id = fields.Many2one(
        string="Purchase Line",
        comodel_name="purchase.order.line",
        copy=False,
    )
    purchase_id = fields.Many2one(
        string="Purchase Order",
        comodel_name="purchase.order",
        related="purchase_line_id.order_id",
        store=True,
        copy=False,
    )

    @api.depends(
        "product_id",
        "product_id.detailed_type",
        "product_id.variant_seller_ids",
        "product_id.variant_seller_ids.partner_id",
    )
    def _compute_product_supplier_ids(self):
        for line in self:
            suppliers_ids = []
            if line.product_id and line.product_id.variant_seller_ids:
                suppliers_ids = line.product_id.variant_seller_ids.ids
            line.product_supplier_ids = [(6, 0, suppliers_ids)]

    @api.depends("product_id")
    def _compute_product_supplier_id(self):
        for line in self:
            if line.product_id and len(line.product_id.variant_seller_ids) == 1:
                line.product_supplier_id = line.product_id.variant_seller_ids[0].id

    def action_create_purchase_order_for_service(self):
        for line in self.filtered(
            lambda x: x.product_supplier_id and not x.purchase_id
        ):
            line.create_purchase_order_for_product()

    def create_purchase_order_for_product(self):
        purchase_obj = self.env["purchase.order"]
        purchase_line_obj = self.env["purchase.order.line"]
        cond = [
            ("partner_id", "=", self.supplier_id.id),
            ("origin", "=", self.order_id.name),
        ]
        purchase = purchase_obj.search(cond, limit=1)
        if not purchase:
            values = self._values_for_create_purchase_order_for_product()
            newpurchase = purchase_obj.new(values)
            for comp_onchange in newpurchase._onchange_methods["partner_id"]:
                comp_onchange(newpurchase)
            vals = newpurchase._convert_to_write(newpurchase._cache)
            purchase = purchase_obj.create(vals)
        values = self._values_for_create_purchase_order_line_for_product(purchase)
        newpline = purchase_line_obj.new(values)
        for comp_onchange in newpline._onchange_methods["product_id"]:
            comp_onchange(newpline)
        vals = newpline._convert_to_write(newpline._cache)
        purchase_line = purchase_line_obj.create(vals)
        purchase_line.product_qty = self.product_uom_qty
        if self.ref_catalogue:
            purchase_line.name = "{} {}".format(self.ref_catalogue, purchase_line.name)
        self.purchase_line_id = purchase_line.id

    def _values_for_create_purchase_order_for_product(self):
        values = {
            "partner_id": self.supplier_id.id,
            "origin": self.order_id.name,
        }
        return values

    def _values_for_create_purchase_order_line_for_product(self, purchase):
        values = {
            "order_id": purchase.id,
            "product_id": self.product_id.id,
            "product_qty": 0,
            "sale_line_id": self.id,
        }
        return values
