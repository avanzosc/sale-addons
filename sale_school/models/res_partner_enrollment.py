# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

ENROLL_ACTION = [
    ("pass", "Next Course"),
    ("repeat", "Repeat Course"),
    ("unenroll", "Unenroll"),
]


class ResPartnerEnrollment(models.Model):
    _name = "res.partner.enrollment"
    _description = "Partner Enrollment History"

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Student", required=True,
        domain=[("educational_category", "=", "student")])
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Next Academic Year",
        required=True)
    enrollment_action = fields.Selection(
        selection=ENROLL_ACTION, string="Enrollment Action", required=True)
    enrollment_course_id = fields.Many2one(
        comodel_name="education.course", string="Next Enrollment Course")
    enrollment_center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")])
    enrollment_state = fields.Selection(
        selection=[("pending", "Pending"),
                   ("processed", "Processed"),
                   ("errored", "Errored")], string="Enrollment State",
        default="pending", required=True)

    _sql_constraints = [(
        "partner_academic_year_unique",
        "unique(partner_id, academic_year_id)",
        "There can be only one definition per year and student")]

    @api.multi
    def create_enrollment(self):
        course_change_obj = self.env["education.course.change"]
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True),
        ])
        next_year = current_year and current_year._get_next()
        for enrollment in self.filtered(
                lambda e: e.academic_year_id == next_year and
                e.enrollment_state == "pending"):
            if enrollment.enrollment_action in ("pass", "repeat"):
                if enrollment.enrollment_action == "pass":
                    course_change = course_change_obj.search([
                        ("school_id", "=",
                         enrollment.partner_id.current_center_id.id),
                        ("course_id", "=",
                         enrollment.partner_id.current_course_id.id),
                        ("next_school_id", "=",
                         enrollment.enrollment_center_id.id),
                        ("next_course_id", "=",
                         enrollment.enrollment_course_id.id),
                    ])
                    if not course_change:
                        enrollment.enrollment_state = "errored"
                        continue
                enrollment.partner_id.create_enrollment(
                    enrollment.academic_year_id,
                    enrollment.enrollment_center_id,
                    enrollment.enrollment_course_id)
            elif enrollment.enrollment_action == "unenroll":
                enrollment.partner_id.action_discontinue()
                enrollment.enrollment_state = "processed"
