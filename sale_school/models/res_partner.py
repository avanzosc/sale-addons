# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
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
    enrollment_history_ids = fields.One2many(
        comodel_name="res.partner.enrollment", inverse_name="partner_id",
        string="Enrollment History", readonly=True)

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
    def action_discontinue(self):
        self.ensure_one()
        if self.educational_category not in ("student", "otherchild"):
            return
        current_group = self.get_current_group()
        self.write({
            "educational_category": "otherrelative",
            "old_student": True,
            "alumni_center_id": current_group.center_id.id,
            "alumni_academic_year_id": current_group.academic_year_id.id,
            "current_center_id": False,
            "current_level_id": False,
            "current_course_id": False,
            "current_group_id": False,
        })
        self.message_post(
            body=_("Student's registration has been discharged."))

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
        next_year_enroll = self.enrollment_history_ids.filtered(
            lambda e: e.academic_year_id == next_year)
        next_year_enroll.create_enrollment()

    @api.multi
    def create_enrollment(self, next_year, center, course):
        self.ensure_one()
        if self.educational_category not in ("student", "otherchild"):
            return
        self.env["sale.order"].find_or_create_enrollment(
            self, next_year, center, course)
        return True
