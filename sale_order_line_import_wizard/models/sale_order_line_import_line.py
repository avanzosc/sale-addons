# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import unicodedata

from odoo import _, fields, models
from odoo.exceptions import UserError

ATTRIBUTE_FIELDS = {
    "SHAPE": "shape",
    "TOP": "color_top",
    "M2": "color_m2",
    "M3": "color_m3",
    "M4": "color_m4",
    "M5": "color_m5",
    "M6": "color_m6",
    "BOTTOM": "color_bottom",
    "FINISH": "finish",
    "Top Graphic": "top_graphic_type",
    "Bottom Graphic": "bottom_graphic_type",
    "Top Foil": "top_foil",
    "Bottom Foil": "bottom_foil",
    "Top Laser": "top_laser",
    "Bottom Laser": "bottom_laser",
    "DECK SRINKWRAP": "deck_shrinkwrap",
    "Sticker OEM": "sticker",
    "Warranty OEM": "warranty",
}

CUSTOM_FIELDS = {
    "Top Graphic": "top_graphic_name",
    "Bottom Graphic": "bottom_graphic_name",
    "Top Laser": "top_laser_name",
    "Bottom Laser": "bottom_laser_name",
    "Sticker OEM": "sticker_name",
    "Warranty OEM": "warranty_name",
}


def normalized(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in value if not unicodedata.combining(char)).casefold()


class SaleOrderLineImportLine(models.Model):
    _name = "sale.order.line.import.line"
    _inherit = "base.import.line"
    _description = "Sale order line import line"
    _order = "id"

    import_id = fields.Many2one(
        comodel_name="sale.order.line.import",
        required=True,
        ondelete="cascade",
    )
    order_id = fields.Many2one(related="import_id.order_id", store=True)
    action = fields.Selection(
        selection_add=[("create", "Create")], ondelete={"create": "set default"}
    )
    product_template_name = fields.Char(string="Product Template")
    product_tmpl_id = fields.Many2one(comodel_name="product.template", copy=False)
    product_id = fields.Many2one(comodel_name="product.product", copy=False)
    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line", copy=False, readonly=True
    )
    config_session_id = fields.Many2one(
        comodel_name="product.config.session", copy=False, readonly=True
    )
    quantity = fields.Float()
    price_unit = fields.Float()
    total = fields.Float()
    shape = fields.Char()
    color_top = fields.Char(string="Top color")
    color_m2 = fields.Char(string="M2 color")
    color_m3 = fields.Char(string="M3 color")
    color_m4 = fields.Char(string="M4 color")
    color_m5 = fields.Char(string="M5 color")
    color_m6 = fields.Char(string="M6 color")
    color_bottom = fields.Char(string="Bottom color")
    finish = fields.Char()
    top_graphic_type = fields.Char()
    top_graphic_name = fields.Char()
    bottom_graphic_type = fields.Char()
    bottom_graphic_name = fields.Char()
    top_foil = fields.Char()
    bottom_foil = fields.Char()
    top_laser = fields.Char()
    top_laser_name = fields.Char()
    bottom_laser = fields.Char()
    bottom_laser_name = fields.Char()
    deck_shrinkwrap = fields.Char(string="Deck shrinkwrap")
    sticker = fields.Char()
    sticker_name = fields.Char()
    warranty = fields.Char()
    warranty_name = fields.Char()
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value", copy=False, readonly=True
    )
    custom_values = fields.Json(copy=False, readonly=True)

    def _find_template(self):
        templates = self.env["product.template"].search(
            [("name", "=ilike", self.product_template_name)]
        )
        if not templates:
            return templates, _("Product template '%s' was not found.") % (
                self.product_template_name,
            )
        if len(templates) > 1:
            return templates, _("More than one product template named '%s' exists.") % (
                self.product_template_name,
            )
        return templates, ""

    def _find_attribute_line(self, template, attribute_name):
        return template.attribute_line_ids.filtered(
            lambda line: normalized(line.attribute_id.name)
            == normalized(attribute_name)
        )

    def _find_attribute_value(self, line, source_value):
        source = str(source_value or "").strip()
        if not source:
            return self.env["product.attribute.value"]
        candidates = line.value_ids
        source_normalized = normalized(source)
        result = candidates.filtered(
            lambda value: normalized(value.name) == source_normalized
        )
        if not result and "code" in candidates._fields:
            codes = {source_normalized}
            if source.isdigit():
                codes.add(source.zfill(2).casefold())
            result = candidates.filtered(lambda value: normalized(value.code) in codes)
        return result

    def _yes_no_value(self, name):
        return str(name or "No").strip().capitalize()

    def _configuration_data(self, template):
        errors = []
        value_ids = []
        custom_values = {}
        for attribute_name, field_name in ATTRIBUTE_FIELDS.items():
            source_value = getattr(self, field_name)
            if attribute_name in ("Sticker OEM", "Warranty OEM"):
                source_value = self._yes_no_value(source_value)
            if not source_value:
                continue
            attribute_line = self._find_attribute_line(template, attribute_name)
            if not attribute_line:
                errors.append(
                    _("Attribute '%s' is not configured on the product template.")
                    % attribute_name
                )
                continue
            attribute_value = self._find_attribute_value(attribute_line, source_value)
            if not attribute_value:
                errors.append(
                    _("Value '%(value)s' was not found for attribute '%(attribute)s'.")
                    % {"value": source_value, "attribute": attribute_name}
                )
                continue
            value_ids.append(attribute_value.id)
        for attribute_name, field_name in CUSTOM_FIELDS.items():
            custom_value = getattr(self, field_name)
            if not custom_value:
                continue
            attribute_line = self._find_attribute_line(template, attribute_name)
            if not attribute_line:
                errors.append(
                    _("Attribute '%s' is not configured on the product template.")
                    % attribute_name
                )
                continue
            custom_values[str(attribute_line.attribute_id.id)] = custom_value
        return list(set(value_ids)), custom_values, errors

    def _action_validate(self):
        self.ensure_one()
        errors = []
        if not self.order_id or self.order_id.state not in ("draft", "sent"):
            errors.append(_("The line import requires a draft quotation."))
        if not self.product_template_name:
            errors.append(_("The product template is required."))
            template = self.env["product.template"]
        else:
            template, template_error = self._find_template()
            if template_error:
                errors.append(template_error)
        value_ids, custom_values, config_errors = self._configuration_data(template)
        errors += config_errors
        if self.quantity <= 0:
            errors.append(_("Quantity must be greater than zero."))
        return {
            "product_tmpl_id": template.id if len(template) == 1 else False,
            "attribute_value_ids": [(6, 0, value_ids)],
            "custom_values": custom_values,
            "action": "create",
            "state": "error" if errors else "pass",
            "log_info": "\n".join(errors),
        }

    def _prepare_sale_order_line_values(self, session):
        configurator = self.env["product.configurator.sale"].new(
            {"order_id": self.order_id.id, "config_session_id": session.id}
        )
        values = configurator._get_order_line_vals(session.product_id.id)
        line_model = self.env["sale.order.line"]
        fields_spec = session.get_onchange_specifications(model="sale.order.line")
        fields_spec = {key: val for key, val in fields_spec.items() if key in values}
        updates = line_model.onchange(values, ["product_id"], fields_spec)
        onchange_values = session.get_vals_to_write(
            values=updates.get("value", {}), model="sale.order.line"
        )
        onchange_values.update(values)
        onchange_values.update(
            {
                "product_uom_qty": self.quantity,
                "price_unit": self.price_unit,
            }
        )
        return onchange_values

    def _action_process(self):
        self.ensure_one()
        if self.action != "create":
            return super()._action_process()
        if self.sale_order_line_id:
            return {"state": "done"}
        session_values = {
            "product_tmpl_id": self.product_tmpl_id.id,
            "user_id": self.env.uid,
            "value_ids": [(6, 0, self.attribute_value_ids.ids)],
        }
        session = self.env["product.config.session"].create(session_values)
        if self.custom_values:
            session.write(
                {
                    "custom_value_ids": [
                        (
                            0,
                            0,
                            {"attribute_id": int(attribute_id), "value": value},
                        )
                        for attribute_id, value in self.custom_values.items()
                    ]
                }
            )
        try:
            session.action_confirm()
            line = self.env["sale.order.line"].create(
                self._prepare_sale_order_line_values(session)
            )
        except Exception:
            session.unlink()
            raise
        return {
            "state": "done",
            "log_info": "",
            "config_session_id": session.id,
            "product_id": session.product_id.id,
            "sale_order_line_id": line.id,
        }

    def unlink(self):
        processed = self.filtered("sale_order_line_id")
        if processed:
            raise UserError(_("Processed import lines cannot be deleted."))
        return super().unlink()
