# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from ..models.res_partner_enrollment import ENROLL_ACTION


class EducationEnrollment(models.TransientModel):
    _name = "education.enrollment"
    _description = "Enrollment Wizard"

    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Next Academic Year")
    line_ids = fields.One2many(
        comodel_name="education.enrollment.line", inverse_name="enrollment_id",
        string="Enrollment Lines")

    @api.model
    def default_get(self, fields):
        result = super(EducationEnrollment, self).default_get(fields)
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True),
        ])
        next_year = current_year._get_next()
        result.update({
            "academic_year_id": next_year.id,
        })
        if self.env.context.get("active_model") == "res.partner":
            active_ids = self.env.context.get("active_ids")
            partners = self.env["res.partner"].browse(active_ids)
            enroll_partner = self.env["res.partner.enrollment"].search([
                ("academic_year_id", "=", next_year.id),
                ("partner_id", "in", active_ids),
            ])
            partner_list = partners.filtered(
                lambda p: p not in enroll_partner.mapped("partner_id") and
                p.educational_category == "student")
            enroll_obj = self.env["education.enrollment.line"]
            lines = []
            for partner in partner_list:
                group = partner.get_current_group()
                course_changes = self.env["education.course.change"].search([
                    ("school_id", "=", group.center_id.id),
                    ("course_id", "=", group.course_id.id)
                ])
                enroll_action = "unenroll" if not course_changes else "pass"
                new_enroll = enroll_obj.new({
                    "partner_id": partner.id,
                    "enroll_action": enroll_action,
                    "current_center_id": group.center_id.id,
                    "current_course_id": group.course_id.id,
                })
                for onchange_method in new_enroll._onchange_methods[
                        'enroll_action']:
                    onchange_method(new_enroll)
                new_enroll_dict = new_enroll._convert_to_write(
                    new_enroll._cache)
                lines.append((0, 0, new_enroll_dict))
            result.update({
                "line_ids": lines,
            })
        return result

    @api.multi
    def button_create_enrollment(self):
        self.mapped("line_ids").create_partner_enrollment()
        return {"type": "ir.actions.act_window_close"}


class EducationEnrollmentLine(models.TransientModel):
    _name = "education.enrollment.line"
    _description = "Enrollment Wizard Line"

    enrollment_id = fields.Many2one(
        comodel_name="education.enrollment", string="Enrollment Wizard",
        required=True, ondelete="cascade")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")], required=True,
        ondelete="cascade")
    current_center_id = fields.Many2one(
        comodel_name="res.partner", string="Current Education Center")
    current_course_id = fields.Many2one(
        comodel_name="education.course", string="Current Education Course")
    next_center_id = fields.Many2one(
        comodel_name="res.partner", string="Next Education Center",
        domain=[("educational_category", "=", "school")])
    next_course_id = fields.Many2one(
        comodel_name="education.course", string="Next Education Course")
    enroll_action = fields.Selection(
        selection=ENROLL_ACTION, string="Enroll Action")

    @api.multi
    @api.onchange("enroll_action")
    def _onchange_enroll_action(self):
        group = self.partner_id.get_current_group()
        if self.enroll_action == "pass":
            course_changes = self.env["education.course.change"].search([
                ("school_id", "=", group.center_id.id),
                ("course_id", "=", group.course_id.id),
                "|", ("gender", "=", self.partner_id.gender),
                ("gender", "=", False),
            ])
            possible_next_center_ids = course_changes.mapped(
                "next_school_id")
            possible_next_course_ids = course_changes.mapped(
                "next_course_id")
            if len(possible_next_center_ids) == 1:
                self.next_center_id = possible_next_center_ids[:1]
            if len(possible_next_course_ids) == 1:
                self.next_course_id = possible_next_course_ids[:1]
        elif self.enroll_action == "repeat":
            self.next_center_id = group.center_id
            self.next_course_id = group.course_id
        else:
            self.next_center_id = False
            self.next_course_id = False

    @api.multi
    def create_partner_enrollment(self):
        enroll_obj = self.env["res.partner.enrollment"]
        for line in self.filtered("enroll_action"):
            group = line.partner_id.get_current_group()
            enroll_obj.create({
                "partner_id": line.partner_id.id,
                "center_id": group.center_id.id,
                "course_id": group.course_id.id,
                "academic_year_id": line.enrollment_id.academic_year_id.id,
                "enrollment_action": line.enroll_action,
                "enrollment_center_id": line.next_center_id.id,
                "enrollment_course_id": line.next_course_id.id,
            })
