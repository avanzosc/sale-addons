# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderGroupChange(models.TransientModel):
    _name = "sale.order.group.change"
    _description = "Wizard to change education group in batch"

    sale_order_ids = fields.Many2many(
        comodel_name="sale.order", string="Sale Order List")
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year")
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center")
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course")
    group_id = fields.Many2one(
        comodel_name="education.group", string="Education Group")

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderGroupChange, self).default_get(fields_list)
        if self.env.context.get("active_model") == "sale.order":
            orders = self.env["sale.order"].browse(
                self.env.context.get("active_ids")).filtered(
                    lambda o: o.state in ["draft", "sent"]
                    and o.academic_year_id is not False
                    and o.school_id is not False
                    and o.course_id is not False)
            if not orders:
                raise UserError(
                    _("Please select quotations."))
            academic_years = orders.mapped("academic_year_id")
            if len(academic_years) != 1:
                raise UserError(
                    _("All quotation must be for the same academic year."))
            centers = orders.mapped("school_id")
            if len(centers) != 1:
                raise UserError(
                    _("All quotation must be for the same center."))
            courses = orders.mapped("course_id")
            if len(courses) != 1:
                raise UserError(
                    _("All quotation must be for the same course."))
            res.update({
                "sale_order_ids": [(6, 0, orders.ids)],
                "academic_year_id": academic_years[:1].id,
                "center_id": centers[:1].id,
                "course_id": courses[:1].id,
            })
        return res

    @api.multi
    def button_change_group(self):
        self.ensure_one()
        sale_orders = self.sale_order_ids.filtered(
            lambda o: o.state in ["draft", "sent"]
            and o.academic_year_id == self.academic_year_id
            and o.school_id == self.center_id
            and o.course_id == self.course_id)
        sale_orders.write({
            "edu_group_id": self.group_id.id,
        })
        return {"type": "ir.actions.act_window_close"}
