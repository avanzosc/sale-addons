# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"
    _order = "sequence, name"

    space_ids = fields.Many2many(
        string="Spaces", comodel_name="sale.order.template.space",
        relation="rel_sale_templates_spaces", column1="sale_template_id",
        column2="sale_template_space_id", copy=False,
    )
    sequence = fields.Integer(
        string="Sequence", default=0, copy=False)
    sale_template_line_count = fields.Integer(
        string="# Sale Template Lines",
        compute="_compute_sale_template_line_count"
    )
    sequence_to_view = fields.Integer(
        string="Sequence", compute="_compute_sequence_to_view", store=True,
        copy=False,
    )

    def _compute_sale_template_line_count(self):
        for template in self:
            template.sale_template_line_count = len(
                template.sale_order_template_line_ids)

    @api.depends("sequence")
    def _compute_sequence_to_view(self):
        for template in self:
            template.sequence_to_view = template.sequence

    def action_view_sale_template_lines(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_template_space.action_editabable_template_orders_lines")
        action["domain"] = expression.AND(
            [[("id", "in", self.sale_order_template_line_ids.ids)],
             safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(self._context, create=False)
        return action

    def write(self, vals):
        result = super(SaleOrderTemplate, self).write(vals)
        if "sequence" in vals:
            for template in self:
                template._recalculate_sequence_lines()
        return result

    def action_renumber_lines(self):
        for template in self:
            template._recalculate_sequence_lines()

    def _recalculate_sequence_lines(self):
        count = 0
        for line in self.sale_order_template_line_ids:
            count += 1
            sequence = int("{}{}".format(self.sequence, count))
            line.sequence = sequence
