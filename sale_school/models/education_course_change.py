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

    @api.multi
    def find_or_create_enrollment(self, student, academic_year):
        self.ensure_one()
        sale_order_obj = self.env["sale.order"]
        sale_order = sale_order_obj.search([
            ("partner_id", "=", student.parent_id.id),
            ("child_id", "=", student.id),
            ("school_id", "=", self.next_school_id.id),
            ("course_id", "=", self.next_course_id.id),
            ("academic_year_id", "=", academic_year.id),
            ("state", "!=", "cancel"),
        ])
        if sale_order:
            return sale_order
        new_sale_order = sale_order_obj.with_context(
            default_child_id=student.id).new({
                "partner_id": student.parent_id.id,
                "child_id": student.id,
                "school_id": self.next_school_id.id,
                "course_id": self.next_course_id.id,
                "academic_year_id": academic_year.id,
            })
        for onchange_method in new_sale_order._onchange_methods['partner_id']:
            onchange_method(new_sale_order)
        for onchange_method in new_sale_order._onchange_methods['course_id']:
            onchange_method(new_sale_order)
        for onchange_method in new_sale_order._onchange_methods[
                'sale_order_template_id']:
            onchange_method(new_sale_order)
        sale_order_dict = new_sale_order._convert_to_write(
            new_sale_order._cache)
        sale_order = sale_order_obj.create(sale_order_dict)
        return True
