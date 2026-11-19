# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderSpace(models.Model):
    _name = "sale.order.space"
    _description = "Spaces For Sale Orders"
    _order = "sequence"

    sequence = fields.Integer(
        copy=True,
    )
    name = fields.Char(
        compute="_compute_name",
        store=True,
        copy=False,
    )
    space_id = fields.Many2one(
        string="Space",
        comodel_name="sale.order.template.space",
        copy=True,
    )
    sale_template_id = fields.Many2one(
        string="Sale Order Template",
        comodel_name="sale.order.template",
        copy=True,
        required=True,
    )
    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
        copy=False,
    )
    num_sale_lines = fields.Integer(
        string="Num. Sale lines",
        compute="_compute_num_sale_lines",
    )

    @api.depends("space_id", "sale_template_id")
    def _compute_name(self):
        for sale_space in self:
            name = sale_space.space_id.name if sale_space.space_id else ""
            if sale_space.sale_template_id:
                name = (
                    sale_space.sale_template_id.name
                    if not name
                    else "{}/{}".format(name, sale_space.sale_template_id.name)
                )
            sale_space.name = name

    def _compute_num_sale_lines(self):
        for space in self:
            num_sale_lines = 0
            if space.sale_order_id and space.sale_order_id.order_line:
                lines = space.sale_order_id.order_line.filtered(
                    lambda x: x.sale_order_space_id == space
                )
                num_sale_lines = len(lines)
            space.num_sale_lines = num_sale_lines

    def action_delete_lines(self):
        for space in self:
            lines = space.sale_order_id.order_line.filtered(
                lambda x: x.sale_order_space_id == space
            )
            if lines:
                lines.unlink()
        return True

    def action_create_lines(self):
        for sale_space in self:
            sale_template = sale_space.sale_template_id
            if (
                sale_space.space_id
                and sale_space.space_id not in sale_space.sale_template_id.space_ids
            ):
                sale_template = False
            if sale_template:
                template_lines = self.env["sale.order.template.line"]
                if not sale_space.space_id:
                    template_lines = sale_template.sale_order_template_line_ids
                if sale_space.space_id:
                    for line in sale_template.sale_order_template_line_ids:
                        if not line.space_ids or sale_space.space_id in line.space_ids:
                            template_lines += line
                if template_lines:
                    sale_space._template_lines_to_sale_lines(template_lines)
            sale_space.sale_order_id.action_put_section_in_lines()

    def _template_lines_to_sale_lines(self, template_lines):
        for line in template_lines:
            vals = self._catch_values_to_create_sale_line(line)
            self.env["sale.order.line"].create(vals)

    def _catch_values_to_create_sale_line(self, line):
        vals = {
            "order_id": self.sale_order_id.id,
            "name": line.name,
            "display_type": line.display_type,
            "product_uom_qty": line.product_uom_qty,
            "sale_order_space_id": self.id,
            "sale_order_template_line_sequence": str(line.sequence).zfill(3),
        }
        if line.product_id:
            vals["product_id"] = line.product_id.id
        if line.product_uom_id:
            vals["product_uom"] = line.product_uom_id.id
        return vals
