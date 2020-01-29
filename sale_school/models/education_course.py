# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EducationCourse(models.Model):
    _inherit = "education.course"

    sale_order_template_ids = fields.One2many(
        comodel_name="sale.order.template", string="Quotation Templates",
        inverse_name="course_id")
    sale_order_template_count = fields.Integer(
        compute="_compute_sale_order_template_count",
        string="# Quotation Templates", store=True)

    @api.multi
    @api.depends("sale_order_template_ids")
    def _compute_sale_order_template_count(self):
        for course in self:
            course.sale_order_template_count = len(
                course.sale_order_template_ids)

    @api.multi
    def button_open_sale_order_templates(self):
        self.ensure_one()
        action = self.env.ref("sale_management.sale_order_template_action")
        action_dict = action and action.read()[0] or {}
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update({
            "default_course_id": self.id,
        })
        domain = expression.AND([
            [("course_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
