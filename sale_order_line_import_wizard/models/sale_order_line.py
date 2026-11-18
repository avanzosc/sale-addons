# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from itertools import groupby

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_sale_order_line_multiline_description_variants(self):
        self.ensure_one()
        selected_ptavs = (
            self.product_id.product_template_attribute_value_ids
            | self.product_no_variant_attribute_value_ids._origin
        ).sorted()
        if not selected_ptavs:
            return ""

        custom_values_by_ptav = {
            custom_value.custom_product_template_attribute_value_id: (
                custom_value.custom_value or ""
            ).strip()
            for custom_value in self.product_custom_attribute_value_ids
        }
        description_lines = []
        for attribute, ptavs_group in groupby(
            selected_ptavs, lambda ptav: ptav.attribute_id
        ):
            values = []
            for ptav in ptavs_group:
                normalized_value = ptav.name.strip().casefold()
                if normalized_value == "no":
                    continue
                custom_value = custom_values_by_ptav.get(ptav)
                if custom_value:
                    if normalized_value in {"yes", "si", "sí"}:
                        value = custom_value
                    else:
                        value = f"{ptav.name}: {custom_value}"
                else:
                    value = ptav.name
                if value:
                    values.append(value)
            if values:
                description_lines.append(f"{attribute.name}: {', '.join(values)}")
        return "".join(f"\n{line}" for line in description_lines)
