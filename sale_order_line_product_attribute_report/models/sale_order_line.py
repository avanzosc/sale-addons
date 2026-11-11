# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64

from odoo import models
from odoo.tools import file_open


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_oem_report_background(self):
        with file_open(
            "sale_order_line_product_attribute_report/static/src/img/background.png",
            "rb",
        ) as background:
            return base64.b64encode(background.read())

    def _get_oem_attribute_value(self, attribute_name):
        self.ensure_one()
        template_values = self.product_id.product_template_attribute_value_ids
        values = template_values.product_attribute_value_id
        return values.filtered(
            lambda value: value.attribute_id.name.strip().casefold()
            == attribute_name.strip().casefold()
        )[:1]

    def get_oem_shape(self):
        self.ensure_one()
        return self._get_oem_attribute_value("SHAPE").shape_id

    def get_oem_quantities_shapes(self):
        self.ensure_one()
        shape = self.get_oem_shape()
        quantity = f"{self.product_uom_qty:g}"
        return f"{quantity} X {shape.name if shape else ''}".strip()

    def get_oem_plies(self):
        self.ensure_one()
        return [
            (name, self._get_oem_attribute_value(name))
            for name in ("Top", "M2", "M3", "M4", "M5", "M6", "Bottom")
            if self._get_oem_attribute_value(name)
        ]

    def get_oem_finish(self):
        self.ensure_one()
        return self._get_oem_attribute_value("FINISH")
