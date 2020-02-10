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
        return super(SaleOrder, self).action_confirm()

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
        for sale in self:
            template = template_obj.search([
                ("school_id", "=", sale.school_id.id),
                ("course_id", "=", sale.course_id.id),
            ])
            sale.sale_order_template_id = template[:1]
