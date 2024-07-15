# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.models import expression


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="uom.uom",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date_order = fields.Datetime()
    material = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    grade = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    thickness = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    component_id = fields.Many2one(
        string="Component",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    material_cost = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    operations_costs_part = fields.Char(
        string="Operations Costs/Part",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    weight = fields.Float(
        digits=(14, 6),
        states={"done": [("readonly", True)]},
        copy=False,
    )
    part_size = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    unit_cost = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    total_cost = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _check_product(self):
        self.ensure_one()
        product, log_info_product = self._check_product_name()
        if not product and not log_info_product:
            product, log_info_product = super(
                SaleOrderImportLine, self.with_context(from_sale_wizard_laser=True)
            )._check_product()
        if not self.component_id:
            log_info_product = self._check_component(log_info_product)
        log_info_product = self._check_workcenters(log_info_product)
        return product, log_info_product

    def _check_product_name(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        search_domain = [("name", "=", self.product_code)]
        search_domain = expression.AND(
            [
                [
                    "|",
                    ("company_id", "=", self.import_id.company_id.id),
                    ("company_id", "=", False),
                ],
                search_domain,
            ]
        )
        products = product_obj.search(search_domain)
        if len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        return products, log_info

    def _check_component(self, log_info_product):
        cond = [
            ("product_material_id.name", "=", self.material),
            ("product_grade_id.name", "=", self.grade),
            ("product_thickness_id.name", "=", self.thickness),
        ]
        component = self.env["product.product"].search(cond, limit=1)
        if not component:
            self.component_id = False
            error = _("Component not found.")
            log_info_product = (
                error
                if not log_info_product
                else "{} {}".format(log_info_product, error)
            )
        else:
            self.component_id = component.id if component else False
        return log_info_product

    def _check_workcenters(self, log_info_product):
        workcenters = []
        parts = re.findall(r"\s*([^,]+?)\s*(?=,|$)", self.operations_costs_part)
        for part in parts:
            log_info_product, workcenters = self._check_workcenter(
                part, log_info_product, workcenters
            )
        if "get_workcenters" not in self.env.context:
            return log_info_product
        else:
            return log_info_product, workcenters

    def _check_workcenter(self, part, log_info_product, workcenters):
        pos = part.find(" = ")
        workcenter_name = part[0:pos]
        cond = [("name", "=", workcenter_name)]
        workcenter = self.env["mrp.workcenter"].search(cond, limit=1)
        if not workcenter:
            error = _("Workcenter: %(center)s not found.") % {"center": workcenter_name}
            log_info_product = (
                error
                if not log_info_product
                else "{} {}".format(log_info_product, error)
            )
        else:
            workcenters.append(workcenter)
        return log_info_product, workcenters

    def _action_process(self):
        if self.action == "create":
            self._action_process_product()
            self._action_process_bom()
        return super()._action_process()

    def _action_process_product(self):
        product_obj = self.env["product.product"]
        if not self.product_id:
            product, log_info_product = self._check_product()
            if log_info_product:
                raise UserError(log_info_product)
            else:
                if not product:
                    product = product_obj.create(self._catch_product_values())
                self.product_id = product.id

    def _catch_product_values(self):
        if not self.import_id.product_categ_id:
            raise UserError(_("You must introduce the product category."))
        product_length = 0
        product_width = 0
        product_height = 0
        if self.part_size and " X " in str(self.part_size):
            part_size = str(self.part_size)
            pos = part_size.find(" X ")
            length = part_size[0:pos]
            product_length = float(length)
            width = part_size[pos + 3 :]
            product_width = float(width)
        if self.thickness:
            product_height = float(self.thickness)
        volume = product_length * product_width * product_height
        if not self.product_uom_id and not self.import_id.product_uom_id:
            raise UserError(_("You must introduce the product UoM."))
        uom = (
            self.product_uom_id.id
            if self.product_uom_id
            else self.import_id.product_uom_id
        )
        if not self.import_id.route_ids:
            raise UserError(_("You must introduce the route."))
        if not self.import_id.product_volume_uom_id:
            raise UserError(_("You must introduce the product volume UoM."))
        vals = {
            "name": self.product_name,
            "default_code": self.product_name,
            "detailed_type": "product",
            "categ_id": self.import_id.product_categ_id.id,
            "product_material_id": self.component_id.product_material_id.id,
            "volume_uom_id": self.import_id.product_volume_uom_id.id,
            "weight": self.weight,
            "product_length": product_length,
            "product_width": product_width,
            "product_height": product_height,
            "volume": volume,
            "dimensional_uom_id": uom.id,
            "sale_import_id": self.import_id.id,
            "route_ids": [(6, 0, self.import_id.route_ids.ids)],
        }
        return vals

    def _action_process_bom(self):
        cond = [
            ("bom_id.product_id", "=", self.product_id.id),
            ("product_id", "=", self.component_id.id),
        ]
        bom_line = self.env["mrp.bom.line"].search(cond, limit=1)
        if not bom_line:
            self._create_bom()

    def _create_bom(self):
        vals = self._catch_bom_values()
        self.env["mrp.bom"].create(vals)

    def _catch_bom_values(self):
        bom_line_vals = self._catch_bom_line_values()
        operations_vals = self._catch_operations_values()
        bom_vals = {
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "product_id": self.product_id.id,
            "code": self.product_id.code,
            "sale_import_id": self.import_id.id,
            "bom_line_ids": [(0, 0, bom_line_vals)],
            "operation_ids": operations_vals,
        }
        return bom_vals

    def _catch_bom_line_values(self):
        qty = 1
        density = self.product_id.product_material_id.density
        ratio = self.product_id.volume_uom_id.ratio
        if self.product_id.volume_uom_id.uom_type == "bigger":
            qty = (self.product_id.volume * density) / ratio
        if self.product_id.volume_uom_id.uom_type == "smaller":
            qty = self.product_id.volume * density * ratio
        return {"product_id": self.component_id.id, "product_qty": qty}

    def _catch_operations_values(self):
        operation_vals = []
        log_info_center, workcenters = self.with_context(
            get_workcenters=True
        )._check_workcenters("")
        if log_info_center:
            raise UserError(log_info_center)
        for workcenter in workcenters:
            center_vals = self._get_workcenter_values(workcenter)
            operation_vals.append((0, 0, center_vals))
        return operation_vals

    def _get_workcenter_values(self, workcenter):
        vals = {
            "name": workcenter.name,
            "workcenter_id": workcenter.id,
            "time_mode": "manual",
            "time_cycle_manual": 0,
        }
        return vals
