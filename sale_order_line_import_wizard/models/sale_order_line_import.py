# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64

import xlrd

from odoo import _, api, fields, models

from odoo.addons.base_import_wizard.models.base_import import convert2str


def normalize_code(value):
    if value in (False, None, ""):
        return ""
    return convert2str(value).strip()


def laser_values(value):
    name = str(value or "").strip()
    return ("Yes" if name else "No"), name


class SaleOrderLineImport(models.Model):
    _name = "sale.order.line.import"
    _inherit = "base.import"
    _description = "Sale order line import"

    _import_columns = (
        "QTY",
        "PRICE",
        "TOTAL",
        "SHAPE",
        "PRODUCTO/ARTICULO",
        "TP",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "BT",
        "FINISH",
        "RAL",
        "TOP LASER",
        "BOTTOM LASER",
        "TOP GRAPHIC TYPE",
        "TOP GRAPHIC NAME",
        "TOP FOIL",
        "BOTTOM GRAPHIC TYPE",
        "BOTTOM GRAPHIC NAME",
        "BOTTOM FOIL",
        "DECK SRINKWRAP",
        "STICKER",
        "STICKER NAME",
        "WARRANTY",
        "WARRANTY NAME",
    )
    _complete_import_columns = _import_columns + (
        "WHEEL MOULD",
        "WHEEL HARDNESS",
        "WHEEL FORMULA",
        "WHEEL LABEL",
        "WHEEL STICKER",
        "WHEEL PACKAGING",
        "WHEEL GRAPHIC SETUP",
        "TRUCK TYPE",
        "TRUCK PRINT",
    )

    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
        required=True,
        index=True,
        copy=False,
        ondelete="cascade",
    )
    company_id = fields.Many2one(related="order_id.company_id", store=True)
    import_type = fields.Selection(
        selection=[("deck", "Deck"), ("complete", "Complete")],
        required=True,
        default="deck",
        copy=False,
    )
    import_line_ids = fields.One2many(
        comodel_name="sale.order.line.import.line",
        inverse_name="import_id",
    )
    sale_order_line_count = fields.Integer(compute="_compute_sale_order_line_count")

    @api.depends("import_line_ids.sale_order_line_id")
    def _compute_sale_order_line_count(self):
        for record in self:
            record.sale_order_line_count = len(
                record.import_line_ids.sale_order_line_id
            )

    def _row_value(self, row_values, *names):
        for name in names:
            if name in row_values:
                return row_values[name]
        return ""

    def _read_xls(self):
        self.ensure_one()
        workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.data))
        sheet_name = "DECK" if self.import_type == "deck" else "Complete"
        sheet = (
            workbook.sheet_by_name(sheet_name)
            if sheet_name in workbook.sheet_names()
            else workbook.sheet_by_index(0)
        )
        columns = (
            self._complete_import_columns
            if self.import_type == "complete"
            else self._import_columns
        )
        lines = []
        product_template_name = ""
        for row_number in range(2, sheet.nrows):
            row = sheet.row_values(row_number, 0, end_colx=len(columns))
            row_values = dict(zip(columns, row, strict=True))
            if not self._row_value(row_values, "QTY") and not self._row_value(
                row_values, "SHAPE"
            ):
                continue
            row_product = self._row_value(
                row_values, "PRODUCTO/ARTICULO", "PRODUCTO ARTICULO", "PRODUCT"
            )
            if row_product:
                product_template_name = row_product
            else:
                row_values["PRODUCTO/ARTICULO"] = product_template_name
            line_values = self._get_line_values(row_values, datemode=workbook.datemode)
            if line_values:
                lines.append((0, 0, line_values))
        return lines

    _read_xlsx = _read_xls

    def _get_line_values(self, row_values, datemode=False):
        values = super()._get_line_values(row_values, datemode=datemode)
        if not values or not row_values:
            return values
        product_template_name = self._row_value(
            row_values, "PRODUCTO/ARTICULO", "PRODUCTO ARTICULO", "PRODUCT"
        )
        shape = self._row_value(row_values, "SHAPE")
        quantity = self._row_value(row_values, "QTY", "QUANTITY")
        price_unit = self._row_value(row_values, "PRICE", "UNIT PRICE")
        top_laser, top_laser_name = laser_values(
            self._row_value(row_values, "TOP LASER")
        )
        bottom_laser, bottom_laser_name = laser_values(
            self._row_value(row_values, "BOTTOM LASER")
        )
        if not any((product_template_name, shape, quantity, price_unit)):
            return False
        values.update(
            {
                "product_template_name": str(product_template_name or "").strip(),
                "quantity": quantity or 0.0,
                "price_unit": price_unit or 0.0,
                "total": self._row_value(row_values, "TOTAL") or 0.0,
                "shape": normalize_code(shape),
                "color_top": normalize_code(self._row_value(row_values, "TP")),
                "color_m2": normalize_code(self._row_value(row_values, "M2")),
                "color_m3": normalize_code(self._row_value(row_values, "M3")),
                "color_m4": normalize_code(self._row_value(row_values, "M4")),
                "color_m5": normalize_code(self._row_value(row_values, "M5")),
                "color_m6": normalize_code(self._row_value(row_values, "M6")),
                "color_bottom": normalize_code(self._row_value(row_values, "BT")),
                "finish": normalize_code(self._row_value(row_values, "FINISH")),
                "ral": normalize_code(self._row_value(row_values, "RAL")),
                "top_graphic_type": str(
                    self._row_value(row_values, "TOP GRAPHIC TYPE", "TOP GRAPHIC") or ""
                ).strip(),
                "top_graphic_name": str(
                    self._row_value(row_values, "TOP GRAPHIC NAME") or ""
                ).strip(),
                "bottom_graphic_type": str(
                    self._row_value(row_values, "BOTTOM GRAPHIC TYPE", "BOTTOM GRAPHIC")
                    or ""
                ).strip(),
                "bottom_graphic_name": str(
                    self._row_value(row_values, "BOTTOM GRAPHIC NAME") or ""
                ).strip(),
                "top_foil": normalize_code(self._row_value(row_values, "TOP FOIL")),
                "bottom_foil": normalize_code(
                    self._row_value(row_values, "BOTTOM FOIL")
                ),
                "top_laser": top_laser,
                "top_laser_name": top_laser_name,
                "bottom_laser": bottom_laser,
                "bottom_laser_name": bottom_laser_name,
                "deck_shrinkwrap": normalize_code(
                    self._row_value(row_values, "DECK SRINKWRAP", "DECK SHRINKWRAP")
                ),
                "sticker": normalize_code(self._row_value(row_values, "STICKER")),
                "sticker_name": str(
                    self._row_value(row_values, "STICKER NAME") or ""
                ).strip(),
                "warranty": normalize_code(self._row_value(row_values, "WARRANTY")),
                "warranty_name": str(
                    self._row_value(row_values, "WARRANTY NAME") or ""
                ).strip(),
                "wheel_mould": normalize_code(
                    self._row_value(row_values, "WHEEL MOULD")
                ),
                "wheel_hardness": normalize_code(
                    self._row_value(row_values, "WHEEL HARDNESS")
                ),
                "wheel_formula": normalize_code(
                    self._row_value(row_values, "WHEEL FORMULA")
                ),
                "wheel_label": normalize_code(
                    self._row_value(row_values, "WHEEL LABEL")
                ),
                "wheel_sticker": normalize_code(
                    self._row_value(row_values, "WHEEL STICKER")
                ),
                "wheel_packaging": normalize_code(
                    self._row_value(row_values, "WHEEL PACKAGING")
                ),
                "wheel_graphic_setup": normalize_code(
                    self._row_value(row_values, "WHEEL GRAPHIC SETUP")
                ),
                "truck_type": normalize_code(self._row_value(row_values, "TRUCK TYPE")),
                "truck_print": normalize_code(
                    self._row_value(row_values, "TRUCK PRINT")
                ),
            }
        )
        return values

    def action_open_sale_order_lines(self):
        self.ensure_one()
        return {
            "name": _("Imported Sale Order Lines"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order.line",
            "view_mode": "list,form",
            "domain": [("id", "in", self.import_line_ids.sale_order_line_id.ids)],
        }
