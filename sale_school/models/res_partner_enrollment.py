# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

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
    partner_parent_id = fields.Many2one(
        comodel_name="res.partner", string="Family",
        related="partner_id.parent_id", store=True)
    partner_birthdate = fields.Date(
        string="Student Birthdate", related="partner_id.birthdate_date",
        store=True)
    partner_child_number = fields.Integer(
        string="Child Number", related="partner_id.child_number", store=True,
        help="This field defines the child position over enrollees from the "
             "same family")
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
    errored_note = fields.Text(string="Errored Note")
    is_exception = fields.Boolean(string="Exception")
    exception_note = fields.Text(string="Exception Note")

    _sql_constraints = [(
        "partner_academic_year_unique",
        "unique(partner_id, academic_year_id)",
        "There can be only one definition per year and student")]

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, "[{}] {}".format(
                record.academic_year_id.name, record.partner_id.display_name)))
        return result

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
        self.write({
            "state": "pending",
        })

    @api.multi
    def mark_exception(self):
        self.ensure_one()
        self.filtered(lambda e: e.state == "errored").write({
            "state": "pending",
            "is_exception": True,
        })

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
                if (not enrollment.is_exception and
                        enrollment.enrollment_action == "pass"):
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
                        enrollment.write({
                            "state": "errored",
                            "errored_note": _("No Course Change defined"),
                        })
                        continue
                enrollment.partner_id.create_enrollment(
                    enrollment.academic_year_id,
                    enrollment.enrollment_center_id,
                    enrollment.enrollment_course_id)
            elif enrollment.enrollment_action == "unenroll":
                enrollment.partner_id.action_discontinue()
            enrollment.write({
                "state": "processed",
                "errored_note": False,
            })

    @api.multi
    def button_open_enrollment_order(self):
        self.ensure_one()
        action = self.env.ref("sale.action_quotations_with_onboarding")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("child_id", "=", self.partner_id.id),
             ("academic_year_id", "=", self.academic_year_id.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
