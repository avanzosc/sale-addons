# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.depends('order_ids')
    def _compute_sale_amount_total(self):
        for lead in self:
            try:
                super(CrmLead, self)._compute_sale_amount_total()
            except Exception:
                total = 0.0
                nbr = 0
                company_currency = (
                    lead.company_currency or
                    self.env.user.company_id.currency_id)
                for order in lead.order_ids:
                    if order.state in ('draft', 'sent'):
                        nbr += 1
                    if order.state not in ('draft', 'sent', 'cancel'):
                        total += order.currency_id._convert(
                            order.amount_untaxed, company_currency,
                            order.company_id or self.env.user.company_id,
                            order.date_order or fields.Date.today())
                lead.sale_amount_total = total
                lead.sale_number = nbr

    @api.multi
    def find_or_create_enrollment(
            self, student, academic_year, center, course):
        enrollment_obj = self.env["crm.lead.future.student"]
        lead = self.search([
            ("partner_id", "=", student.parent_id.id),
            ("type", "=", "lead"),
        ])
        if not lead:
            new_lead = self.new({
                "partner_id": student.parent_id.id,
                "partner_name": student.parent_id.display_name,
            })
            for onchange_method in new_lead._onchange_methods['partner_id']:
                onchange_method(new_lead)
            lead_dict = new_lead._convert_to_write(new_lead._cache)
            lead = self.create(lead_dict)
        enrollment = enrollment_obj.search([
            ("child_id", "=", student.id),
            ("academic_year_id", "=", academic_year.id),
            ("course_id", "=", course.id),
            ("school_id", "=", center.id),
        ])
        if not enrollment:
            new_enrollment = enrollment_obj.new({
                "crm_lead_id": lead.id,
                "child_id": student.id,
                "academic_year_id": academic_year.id,
                "course_id": course.id,
                "school_id": center.id,
            })
            for onchange_method in new_enrollment._onchange_methods[
                    "child_id"]:
                onchange_method(new_enrollment)
            enrollment_dict = new_enrollment._convert_to_write(
                new_enrollment._cache)
            enrollment_obj.create(enrollment_dict)
        return lead

    @api.multi
    def create_sale_order_for_student(self):
        sales = self.mapped(
            "future_student_ids").create_sale_order_for_student()
        action = self.env.ref('sale.action_quotations_with_onboarding')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('id', 'in', sales.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({
            'domain': domain,
        })
        return action_dict


class CrmLeadFutureStudent(models.Model):
    _inherit = 'crm.lead.future.student'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
    sale_order_state = fields.Selection(
        string="Sale Order Status", related="sale_order_id.state",
        store=True)

    @api.multi
    def create_new_student(self, partner_id=False):
        self.ensure_one()
        if self.sale_order_id:
            self.child_id = self.sale_order_id.child_id
        else:
            super(CrmLeadFutureStudent,
                  self).create_new_student(partner_id=partner_id)

    @api.multi
    def create_sale_order_for_student(self):
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True)])
        if not current_year:
            raise UserError(
                _("There should be at least a current academic year"))
        next_year = current_year._get_next()
        sales = sale_obj = self.env["sale.order"]
        futures = self.filtered(
            lambda l: l.child_id and not l.sale_order_id and
            l.academic_year_id in (current_year, next_year))
        if not futures:
            raise UserError(_("There are not future student to register."))
        for future in futures:
            sale_order = sale_obj.find_or_create_enrollment(
                future.child_id, future.academic_year_id, future.school_id,
                future.course_id)
            future.sale_order_id = sale_order
            future.child_id.educational_category = "student"
            sales += future.sale_order_id
        return sales
