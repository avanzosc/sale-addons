# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class EducationCourseChange(models.Model):
    _inherit = "education.course.change"

    @api.multi
    def create_sale_order_template(self):
        templates = tmpl_obj = self.env["sale.order.template"]
        for record in self:
            sale_tmpl = tmpl_obj.search([
                ("school_id", "=", record.school_id.id),
                ("course_id", "=", record.course_id.id),
            ])
            if not sale_tmpl:
                sale_tmpl = tmpl_obj.create({
                    "name": "{} - {}".format(
                        record.school_id.name, record.course_id.display_name),
                    "school_id": record.school_id.id,
                    "course_id": record.course_id.id,
                })
            templates |= sale_tmpl
        action = self.env.ref("sale_management.sale_order_template_action")
        action_dict = action and action.read()[0]
        domain = expression.AND([
            [("id", "in", templates.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
