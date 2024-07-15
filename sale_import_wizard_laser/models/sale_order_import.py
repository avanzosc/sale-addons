# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base_import_wizard.models.base_import import convert2str

try:
    import xlrd

    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

str2date = fields.Date.to_date


class SaleOrderImport(models.Model):
    _inherit = "sale.order.import"

    @api.model
    def _default_product_categ(self):
        return self.env.ref("product.product_category_all")

    @api.model
    def _default_product_uom(self):
        return self.env.ref("uom.product_uom_millimeter")

    @api.model
    def _default_product_volume_uom(self):
        return self.env.ref("sale_import_wizard_laser.product_uom_volume_mm3")

    def _compute_created_products_count(self):
        for i in self:
            i.created_products_count = len(i.created_product_ids)

    def _compute_created_boms_count(self):
        for i in self:
            i.created_boms_count = len(i.created_bom_ids)

    product_categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        default=_default_product_categ,
        copy=False,
    )
    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="uom.uom",
        default=_default_product_uom,
        copy=False,
    )
    product_volume_uom_id = fields.Many2one(
        string="Product Volume Unit",
        comodel_name="uom.uom",
        default=_default_product_volume_uom,
        copy=False,
    )
    route_ids = fields.Many2many(
        string="Routes",
        comodel_name="stock.route",
        relation="rel_saleimport_stock_route",
        column1="sale_import_id",
        column2="stock_route_id",
    )
    created_product_ids = fields.One2many(
        string="Created products",
        comodel_name="product.product",
        inverse_name="sale_import_id",
        copy=False,
    )
    created_bom_ids = fields.One2many(
        string="Created BoMs",
        comodel_name="mrp.bom",
        inverse_name="sale_import_id",
        copy=False,
    )
    created_products_count = fields.Integer(
        string="# Created Products",
        compute="_compute_created_products_count",
    )
    created_boms_count = fields.Integer(
        string="# Created BoMs",
        compute="_compute_created_boms_count",
    )

    def _read_xls(self):
        if "from_sale_wizard_laser" not in self.env.context:
            return super()._read_xls()
        lines = []
        workbook = xlrd.open_workbook(file_contents=base64.decodebytes(self.data))
        sheet_list = workbook.sheet_names()
        for sheet_name in sheet_list:
            sheet = workbook.sheet_by_name(sheet_name)
            if not sheet.nrows:
                continue
            customer_name = sheet.row_values(0, 1, 2)
            customer_order_ref = sheet.row_values(1, 1, 2)
            date_order = sheet.row_values(2, 1, 2)
            keys = [c.value for c in sheet.row(3)]
            for counter in range(4, sheet.nrows):
                row_values = sheet.row_values(counter, 0, end_colx=sheet.ncols)
                values = dict(zip(keys, row_values))
                line_data = self.with_context(
                    customer_name=customer_name[0],
                    order_ref=customer_order_ref[0],
                    date_order=date_order[0],
                )._get_line_values(values, datemode=workbook.datemode)
                if line_data:
                    lines.append((0, 0, line_data))
        return lines

    _read_xlsx = _read_xls

    def _get_line_fields_values(self, row_values):
        if "from_sale_wizard_laser" not in self.env.context:
            return super()._get_line_fields_values(row_values)
        line_vals = {}
        file_name = row_values.get("File Name ", "")
        material = row_values.get("Material ", "")
        grade = row_values.get("Grade", "")
        thickness = row_values.get("Thickness", "")
        operations_costs_part = row_values.get(" Operations Costs /part ", "")
        part_size = row_values.get("Part Size ", "")
        line_vals.update(
            {
                "product_name": convert2str(file_name),
                "material": convert2str(material),
                "grade": convert2str(grade),
                "thickness": convert2str(thickness),
                "quantity": row_values.get("Qty", 0),
                "material_cost": row_values.get("Material Cost ", 0),
                "operations_costs_part": convert2str(operations_costs_part),
                "weight": row_values.get("Weight ", 0),
                "part_size": convert2str(part_size),
                "unit_cost": row_values.get("Unit Cost", 0),
                "total_cost": row_values.get("Total Cost ", 0),
                "price_unit": row_values.get("Unit Cost", 0),
            }
        )
        if "customer_name" in self.env.context:
            line_vals["customer_name"] = self.env.context.get("customer_name", "")
        if "order_ref" in self.env.context:
            line_vals["client_order_ref"] = self.env.context.get("order_ref", "")
        if "date_order" in self.env.context:
            excel_serial_date = self.env.context.get("date_order", False)
            days = int(excel_serial_date)
            fraction = excel_serial_date - days
            adjusted_days = days - 2
            excel_base_date = datetime(1900, 1, 1)
            converted_date = excel_base_date + timedelta(days=adjusted_days)
            seconds_in_day = 24 * 60 * 60
            time_delta = timedelta(seconds=fraction * seconds_in_day)
            converted_datetime = converted_date + time_delta
            line_vals["date_order"] = converted_datetime
        return line_vals

    def button_open_created_products(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_normal_action"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.created_product_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def button_open_created_boms(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("mrp.mrp_bom_form_action")
        action["domain"] = expression.AND(
            [
                [("id", "in", self.created_bom_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action
