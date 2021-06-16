# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
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
        string="Enrollment History")
    additional_product_ids = fields.Many2many(
        comodel_name="product.product", string="Additional Products",
        relation="rel_partner_addproduct", column1="partner_id",
        column2="product_id")

    @api.multi
    def get_payers_info(self):
        self.ensure_one()
        payer_lines = []
        for payer in self.child2_ids.filtered("payer"):
            payer_line = self.env["sale.order.line.payer"].new({
                "payer_id": payer.responsible_id.id,
                "pay_percentage": payer.payment_percentage,
            })
            for onchange_method in payer_line._onchange_methods["payer_id"]:
                onchange_method(payer_line)
            payer_line_dict = payer_line._convert_to_write(
                payer_line._cache)
            payer_lines.append((0, 0, payer_line_dict))
        return payer_lines

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

    @api.multi
    def _create_enrollment_history(self):
        students = self.search([
            ("educational_category", "=", "student"),
        ])
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True)])
        if not current_year:
            return
        next_year = current_year._get_next()
        enrollment_obj = self.env["res.partner.enrollment"]
        for student in students:
            history = student.enrollment_history_ids.filtered(
                lambda e: e.academic_year_id == next_year)
            if not history:
                new_history = enrollment_obj.new({
                    "academic_year_id": next_year.id,
                    "partner_id": student.id,
                    "enrollment_action": "pass",
                })
                for onchange_method in new_history._onchange_methods[
                        "partner_id"]:
                    onchange_method(new_history)
                for onchange_method in new_history._onchange_methods[
                        "enrollment_action"]:
                    onchange_method(new_history)
                enrolment_dict = new_history._convert_to_write(
                    new_history._cache)
                enrollment_obj.create(enrolment_dict)
        action = self.env.ref("sale_school.action_res_partner_enrollment")
        action_dict = action and action.read()[0]
        domain = expression.AND([
            [("academic_year_id", "=", next_year.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    @api.multi
    def update_pricelist_child_number(self):
        pricelist_obj = self.env["product.pricelist"]
        for partner in self.filtered("child_number"):
            pricelist = partner.property_product_pricelist
            if pricelist and pricelist.type_id:
                new_pricelist = pricelist_obj.search([
                    ("type_id", "=", pricelist.type_id.id),
                    ("child_num", "<=", partner.child_number),
                ], limit=1, order="child_num DESC")
                if new_pricelist and new_pricelist != pricelist:
                    partner.property_product_pricelist = new_pricelist
