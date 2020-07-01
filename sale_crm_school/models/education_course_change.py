# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class EducationCourseChange(models.Model):
    _inherit = "education.course.change"

    @api.multi
    def find_or_create_enrollment(self, student, academic_year):
        self.ensure_one()
        if self.school_id == self.next_school_id:
            return super(
                EducationCourseChange, self).find_or_create_enrollment(
                    student, academic_year)
        lead_obj = self.env["crm.lead"]
        enrollment_obj = self.env["crm.lead.future.student"]
        lead = lead_obj.search([
            ("partner_id", "=", student.parent_id.id),
            ("type", "=", "lead"),
        ])
        if not lead:
            new_lead = lead_obj.new({
                "partner_id": student.parent_id.id,
                "partner_name": student.parent_id.display_name,
            })
            for onchange_method in new_lead._onchange_methods['partner_id']:
                onchange_method(new_lead)
            lead_dict = new_lead._convert_to_write(new_lead._cache)
            lead = lead_obj.create(lead_dict)
        enrollment = enrollment_obj.search([
            ("child_id", "=", student.id),
            ("academic_year_id", "=", academic_year.id),
            ("course_id", "=", self.next_course_id.id),
            ("school_id", "=", self.next_school_id.id),
        ])
        if not enrollment:
            new_enrollment = enrollment_obj.new({
                "crm_lead_id": lead.id,
                "child_id": student.id,
                "academic_year_id": academic_year.id,
                "course_id": self.next_course_id.id,
                "school_id": self.next_school_id.id,
            })
            for onchange_method in new_enrollment._onchange_methods[
                    "child_id"]:
                onchange_method(new_enrollment)
            enrollment_dict = new_enrollment._convert_to_write(
                new_enrollment._cache)
            enrollment_obj.create(enrollment_dict)
        return True
