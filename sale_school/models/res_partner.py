# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartner(models.Model):
    _inherit = "res.partner"

    enrollment_ids = fields.One2many(
        comodel_name="sale.order", inverse_name="child_id",
        string="Enrollments")
    enrollment_count = fields.Integer(
        compute="_compute_enrollment_count", string="# Enrollments",
        compute_sudo=True, store=True)

    @api.multi
    @api.depends("enrollment_ids", "enrollment_ids.state")
    def _compute_enrollment_count(self):
        for record in self.filtered("enrollment_ids"):
            record.enrollment_count = len(
                record.enrollment_ids.filtered(lambda e: e.state != "cancel"))

    @api.multi
    def button_open_enrollments(self):
        self.ensure_one()
        action = self.env.ref("sale.action_quotations_with_onboarding")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update({
            "default_child_id": self.id,
        })
        domain = expression.AND([
            [("child_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict

    @api.multi
    def create_next_enrollment(self):
        self.ensure_one()
        if self.educational_category not in ("student", "otherchild"):
            return
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True)])
        if not current_year:
            return
        next_year = current_year._get_next()
        current_group = self.get_current_group()
        course_changes = self.env["education.course.change"].search([
            ("school_id", "=", current_group.center_id.id),
            ("course_id", "=", current_group.course_id.id),
            "|", ("gender", "=", self.gender), ("gender", "=", False)
        ])
        if not course_changes:
            raise UserError(_("There is not course change defined."))
        for course_change in course_changes:
            course_change.find_or_create_enrollment(self, next_year)
