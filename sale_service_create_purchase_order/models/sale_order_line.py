# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_supplier_ids = fields.Many2many(
        string="Product suppliers", comodel_name="product.supplierinfo",
        compute="_compute_product_supplier_ids",
    )
    product_supplier_id = fields.Many2one(
        string="Product Supplier", comodel_name="product.supplierinfo",
        compute="_compute_product_supplier_id", store=True, readonly=False,
        precompute=True, copy=False,
    )
    supplier_id = fields.Many2one(
        string="Supplier", related="product_supplier_id.partner_id",
        store=True, copy=False,
    )
    detailed_type = fields.Selection(
        string="Product Type", related="product_id.detailed_type",
    )
    ref_catalogue = fields.Char(
        string="Ref. Catalogue", copy=False,
    )
    purchase_line_id = fields.Many2one(
        string="Purchase Line", comodel_name="purchase.order.line", copy=False,
    )
    purchase_id = fields.Many2one(
        string="Purchase Order", comodel_name="purchase.order",
        related="purchase_line_id.order_id", store=True, copy=False
    )
    product_categ_id = fields.Many2one(
        string="Product Category", comodel_name="product.category",
        related="product_id.categ_id", store=True, copy=False,
    )
    sequence_to_view = fields.Integer(
        string="Sequence", related="sequence", store=True, copy=False)

    @api.depends("product_id", "product_id.detailed_type",
                 "product_id.variant_seller_ids",
                 "product_id.variant_seller_ids.partner_id")
    def _compute_product_supplier_ids(self):
        for line in self:
            suppliers_ids = []
            if (line.product_id and
                line.product_id.detailed_type == "service" and
                    line.product_id.variant_seller_ids):
                suppliers_ids = line.product_id.variant_seller_ids.ids
            line.product_supplier_ids = [(6, 0, suppliers_ids)]

    @api.depends("product_id")
    def _compute_product_supplier_id(self):
        for line in self:
            if (line.product_id and
                line.product_id.detailed_type == "service" and
                    len(line.product_id.variant_seller_ids) == 1):
                line.product_supplier_id = (
                    line.product_id.variant_seller_ids[0].id)

    @api.depends("sequence")
    def _compute_sequence_to_view(self):
        for line in self:
            line.sequence_to_view = line.sequence

    def action_create_purchase_order_for_service(self):
        for line in self.filtered(
                lambda x: x.product_supplier_id and not x.purchase_id):
            line.create_purchase_order_for_service()

    def action_duplicate_line(self):
        if len(self) > 1:
            raise ValidationError(
                _("You can only duplicate 1 at a time, because then the screen"
                  "must be refreshed."))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_service_create_purchase_order.wiz_duplicate_sale_line_action")
        return action

    def action_change_sequence(self):
        if len(self) > 1:
            raise ValidationError(
                _("You can only modify 1 sequence, because then the screen"
                  "must be refreshed."))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_service_create_purchase_order.wiz_change_sequence_in_sale_line_action")
        return action

    def create_purchase_order_for_service(self):
        purchase_obj = self.env["purchase.order"]
        purchase_line_obj = self.env["purchase.order.line"]
        cond = [("partner_id", "=", self.supplier_id.id),
                ("origin", "=", self.order_id.name)]
        purchase = purchase_obj.search(cond, limit=1)
        if not purchase:
            values = self._values_for_create_purchase_order_for_service()
            newpurchase = purchase_obj.new(values)
            for (comp_onchange) in (newpurchase._onchange_methods["partner_id"]):
                comp_onchange(newpurchase)
            vals = newpurchase._convert_to_write(newpurchase._cache)
            purchase = purchase_obj.create(vals)
        values = self._values_for_create_purchase_order_line_for_service(
            purchase)
        newpline = purchase_line_obj.new(values)
        for (comp_onchange) in (newpline._onchange_methods["product_id"]):
            comp_onchange(newpline)
        vals = newpline._convert_to_write(newpline._cache)
        purchase_line = purchase_line_obj.create(vals)
        purchase_line.product_qty = self.product_uom_qty
        if self.ref_catalogue:
            purchase_line.name = u"{} {}".format(
                self.ref_catalogue, purchase_line.name)
        self.purchase_line_id = purchase_line.id

    def _values_for_create_purchase_order_for_service(self):
        values = {"partner_id": self.supplier_id.id,
                  "origin": self.order_id.name, }
        return values

    def _values_for_create_purchase_order_line_for_service(self, purchase):
        values = {"order_id": purchase.id,
                  "product_id": self.product_id.id,
                  "product_qty": 0,
                  "sale_line_id": self.id, }
        return values
