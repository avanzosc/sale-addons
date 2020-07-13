# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

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
        domain=[("educational_category", "=", "student")], ondelete="cascade")
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Next Academic Year",
        required=True, ondelete="cascade")
    enrollment_action = fields.Selection(
        selection=ENROLL_ACTION, string="Enrollment Action", required=True)
    possible_course_ids = fields.Many2many(
        comodel_name="education.course", string="Possible Education Courses",
        compute="_compute_possible_courses")
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course")
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")])
    enrollment_course_id = fields.Many2one(
        comodel_name="education.course", string="Enrollment Education Course")
    enrollment_center_id = fields.Many2one(
        comodel_name="res.partner", string="Enrollment Education Center",
        domain=[("educational_category", "=", "school")])
    state = fields.Selection(
        selection=[("pending", "Pending"),
                   ("processed", "Processed"),
                   ("errored", "Errored")], string="Enrollment State",
        default="pending", required=True, readonly=True)

    _sql_constraints = [(
        "partner_academic_year_unique",
        "unique(partner_id, academic_year_id)",
        "There can be only one definition per year and student")]

    @api.multi
    def write(self, values):
        if "state" not in values and any(
                self.mapped(lambda e: e.state == "processed")):
            raise UserError(_("You can't edit processed lines"))
        return super(ResPartnerEnrollment, self).write(values)

    @api.multi
    @api.depends("partner_id", "center_id", "course_id", "enrollment_action")
    def _compute_possible_courses(self):
        course_change_obj = self.env["education.course.change"]
        for enroll in self.filtered(
                lambda e: e.enrollment_action == "pass"):
            course_changes = course_change_obj.search([
                ("school_id", "=", enroll.center_id.id),
                ("course_id", "=", enroll.course_id.id),
                "|", ("gender", "=", enroll.partner_id.gender),
                ("gender", "=", False),
            ])
            enroll.possible_course_ids = course_changes.mapped(
                "next_course_id")

    @api.multi
    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        group = self.partner_id.get_current_group()
        self.center_id = group.center_id
        self.course_id = group.course_id

    @api.multi
    @api.onchange("enrollment_action")
    def _onchange_enroll_action(self):
        if self.enrollment_action == "pass":
            course_changes = self.env["education.course.change"].search([
                ("school_id", "=", self.center_id.id),
                ("course_id", "=", self.course_id.id),
                "|", ("gender", "=", self.partner_id.gender),
                ("gender", "=", False),
            ])
            possible_next_center_ids = course_changes.mapped(
                "next_school_id")
            possible_next_course_ids = course_changes.mapped(
                "next_course_id")
            if len(possible_next_center_ids) == 1:
                self.enrollment_center_id = possible_next_center_ids[:1]
            if len(possible_next_course_ids) == 1:
                self.enrollment_course_id = possible_next_course_ids[:1]
        elif self.enrollment_action == "repeat":
            self.enrollment_center_id = self.center_id
            self.enrollment_course_id = self.course_id
        else:
            self.enrollment_center_id = False
            self.enrollment_course_id = False

    @api.multi
    def button_draft(self):
        self.write({"state": "pending"})

    @api.multi
    def create_enrollment(self):
        course_change_obj = self.env["education.course.change"]
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True),
        ])
        next_year = current_year and current_year._get_next()
        for enrollment in self.filtered(
                lambda e: e.academic_year_id == next_year and
                e.state == "pending"):
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
                        enrollment.state = "errored"
                        continue
                enrollment.partner_id.create_enrollment(
                    enrollment.academic_year_id,
                    enrollment.enrollment_center_id,
                    enrollment.enrollment_course_id)
            elif enrollment.enrollment_action == "unenroll":
                enrollment.partner_id.action_discontinue()
            enrollment.state = "processed"
