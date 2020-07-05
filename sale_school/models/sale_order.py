# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    child_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")],
        index=True, readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        change_default=True, track_visibility="always", track_sequence=1)
    school_id = fields.Many2one(
        comodel_name="res.partner", string="School",
        domain=[("educational_category", "=", "school")],
        index=True, readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]})
    course_id = fields.Many2one(
        comodel_name="education.course", string="Course",
        index=True, readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]})
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic year",
        index=True, readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]})
    edu_group_id = fields.Many2one(
        comodel_name="education.group", string="Education Group",
        index=True, readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]})
    mandatory_subject_ids = fields.Many2many(
        comodel_name="education.subject", string="Mandatory Subjects",
        relation="sale_mandatory_subject_rel", column1="order_id",
        column2="subject_id", readonly=True)
    possible_optional_subject_ids = fields.Many2many(
        comodel_name="education.subject", string="Possible Optional Subjects",
        relation="sale_possible_optional_subject_rel", column1="order_id",
        column2="subject_id", readonly=True)
    optional_subject_ids = fields.Many2many(
        comodel_name="education.subject", string="Optional Subjects",
        relation="sale_optional_subject_rel", column1="order_id",
        column2="subject_id", readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]})

    @api.model
    def create(self, values):
        if values.get("child_id") and not values.get("partner_id"):
            child = self.env["res.partner"].browse(values.get("child_id"))
            values["partner_id"] = child.parent_id.id or child.id
        return super(SaleOrder, self).create(values)

    @api.multi
    def action_confirm(self):
        for sale in self:
            order_lines = sale.mapped("order_line")
            lines = order_lines.filtered(lambda x: x.total_percentage != 100.0)
            if lines:
                raise ValidationError(
                    _("The payers do not add 100%"))
            payers = order_lines.mapped("payer_ids")
            if any(payers.filtered(lambda p: not p.bank_id)):
                raise ValidationError(
                    _("There must be a bank account defined per payer!"))
        res = super(SaleOrder, self).action_confirm()
        for sale in self.filtered("edu_group_id"):
            sale.edu_group_id.student_ids = [(4, sale.child_id.id)]
            sale.child_id.write({
                "current_group_id": sale.edu_group_id.id,
                "current_center_id": sale.edu_group_id.center_id.id,
                "current_course_id": sale.edu_group_id.course_id.id,
            })
        return res

    @api.multi
    @api.onchange("partner_id", "child_id")
    def onchange_partner_id(self):
        self.partner_id = self.child_id.parent_id
        super(SaleOrder, self).onchange_partner_id()
        self.pricelist_id = (
            self.child_id.property_product_pricelist or
            self.partner_id.property_product_pricelist)

    @api.multi
    @api.onchange("school_id", "course_id")
    def onchange_school_course(self):
        template_obj = self.env["sale.order.template"]
        group_obj = self.env["education.group"]
        subject_center_obj = self.env["education.subject.center"]
        for sale in self:
            template = template_obj.search([
                ("school_id", "=", sale.school_id.id),
                ("course_id", "=", sale.course_id.id),
            ])
            sale.sale_order_template_id = template[:1]
            group = group_obj.search([
                ("academic_year_id", "=", sale.academic_year_id.id),
                ("center_id", "=", sale.school_id.id),
                ("course_id", "=", sale.course_id.id),
                ("group_type_id.type", "=", "official")
            ])
            if len(group) == 1:
                sale.edu_group_id = group
            subject_list = subject_center_obj.search([
                ("center_id", "=", sale.school_id.id),
                ("course_id", "=", sale.course_id.id),
            ])
            sale.mandatory_subject_ids = subject_list.filtered(
                lambda l: l.subject_type == "mandatory").mapped("subject_id")
            sale.possible_optional_subject_ids = subject_list.filtered(
                lambda l: l.subject_type == "optional").mapped("subject_id")

    @api.multi
    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        result = super(SaleOrder, self).onchange_sale_order_template_id()
        for line in self.order_line:
            line.payer_ids = line.get_payers_info()
        return result

    def find_or_create_enrollment(
            self, student, academic_year, center, course):
        sale_order = self.search([
            ("partner_id", "=", student.parent_id.id),
            ("child_id", "=", student.id),
            ("academic_year_id", "=", academic_year.id),
            ("state", "!=", "cancel"),
        ])
        if sale_order:
            return sale_order
        new_sale_order = self.with_context(
            default_child_id=student.id).new({
                "partner_id": student.parent_id.id,
                "child_id": student.id,
                "school_id": center.id,
                "course_id": course.id,
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
        sale_order = self.create(sale_order_dict)
        return sale_order

    @api.multi
    def action_cancel(self):
        edu_group_obj = self.env["education.group"]
        res = super(SaleOrder, self).action_cancel()
        for sale in self:
            edu_groups = edu_group_obj.search([
                ("academic_year_id", "=", sale.academic_year_id.id),
                ("center_id", "=", sale.school_id.id),
                ("course_id", "=", sale.course_id.id),
            ])
            for edu_group in edu_groups:
                edu_group.student_ids = [(5, sale.child_id.id)]
            sale.child_id.update_current_group_id()
        return res
