# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from .._common import _catch_top_bottom_graphic_info


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "order_id, bottom_graphic, top_graphic, sequence, id"

    with_all_attributes = fields.Boolean(
        string="With All Attributes",
        compute="_compute_with_all_attributes",
        store=True,
    )
    quantities_shapes = fields.Char(
        string="Quantities & Shapes", compute="_compute_quantities_shapes"
    )
    top_graphic = fields.Char(
        string="Top Graphic", compute="_compute_top_bottom_graphic",
        store=True, copy=False
    )
    bottom_graphic = fields.Char(
        string="Bottom Graphic", compute="_compute_top_bottom_graphic",
        store=True, copy=False
    )

    @api.depends("product_id", "product_id.attribute_value_ids",
                 "product_id.attribute_value_ids.attribute_id",
                 "product_id.attribute_value_ids.attribute_id.name",
                 "product_id.attribute_value_ids.name")
    def _compute_with_all_attributes(self):
        attribute_names = {"Bottom Graphic", "Top Graphic", "TALLA", "SHAPE"}
        for line in self:
            attributes = line.product_id.attribute_value_ids
            line.with_all_attributes = any(
                attr.attribute_id.name in attribute_names for attr in attributes
            )

    def _compute_quantities_shapes(self):
        for line in self:
            quantities_shapes = "%(quantity)s X " % {
                "quantity": line.product_uom_qty,
            }
            attribute = line.product_id.attribute_value_ids.filtered(
                lambda x: x.attribute_id.name == "TALLA")
            if attribute:
                quantities_shapes = "%(quantities_shapes)s %(value)s" % {
                    "quantities_shapes": quantities_shapes,
                    "value": attribute.name,
                }
            attribute = line.product_id.attribute_value_ids.filtered(
                lambda x: x.attribute_id.name == "SHAPE")
            if attribute:
                quantities_shapes = "%(quantities_shapes)s %(shape)s" % {
                    "quantities_shapes": quantities_shapes,
                    "shape": attribute.name,
                }
            line.quantities_shapes = quantities_shapes

    @api.depends("name")
    def _compute_top_bottom_graphic(self):
        for sale_line in self:
            sale_line.top_graphic, sale_line.bottom_graphic = _catch_top_bottom_graphic_info(sale_line)
