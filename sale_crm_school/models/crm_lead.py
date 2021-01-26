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
        current_year = self.env["education.academic_year"].search([
            ("current", "=", True)])
        if not current_year:
            raise UserError(
                _("There should be at least a current academic year"))
        next_year = current_year._get_next()
        sales = self.env['sale.order']
        futures = self.mapped('future_student_ids').filtered(
            lambda l: l.child_id and not l.sale_order_id and
            l.academic_year_id in (current_year, next_year))
        if not futures:
            raise UserError(_('There are not future student to register.'))
        for future in futures:
            vals = future.crm_lead_id.sudo()._get_vals_for_sale_order(future)
            future.sale_order_id = sales.create(vals)
            future.child_id.educational_category = 'student'
            future.crm_lead_id._put_payer_information_in_sale_order(
                future, future.sale_order_id)
            sales += future.sale_order_id
        action = self.env.ref('sale.action_quotations_with_onboarding')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('id', 'in', sales.ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({
            'domain': domain,
        })
        return action_dict

    @api.multi
    def _get_vals_for_sale_order(self, future):
        sale_order_obj = self.env["sale.order"]
        new_sale = sale_order_obj.new({
            "partner_id": self.partner_id.id,
            "opportunity_id": self.id,
            "child_id": future.child_id.id,
            "course_id": future.course_id.id,
            "school_id": future.school_id.id,
            "academic_year_id": future.academic_year_id.id,
        })
        for onchange_method in new_sale._onchange_methods["partner_id"]:
            onchange_method(new_sale)
        for onchange_method in new_sale._onchange_methods["course_id"]:
            onchange_method(new_sale)
        for onchange_method in new_sale._onchange_methods[
                "sale_order_template_id"]:
            onchange_method(new_sale)
        sale_order_dict = new_sale._convert_to_write(
            new_sale._cache)
        return sale_order_dict

    @api.multi
    def _put_payer_information_in_sale_order(self, future, sale):
        for line in sale.order_line:
            vals = {}
            if line.product_id.company_id:
                vals['originator_id'] = line.product_id.company_id.id
            payers = future.child_id.mapped('child2_ids').filtered(
                lambda l: l.payer)
            vals2 = []
            for payer in payers:
                vals2.append(
                    (0, 0, {
                        'child_id': future.child_id.id,
                        'payer_id': payer.responsible_id.id,
                        'pay_percentage': payer.payment_percentage,
                    }))
            if vals2:
                vals['payer_ids'] = vals2
            line.write(vals)


class CrmLeadFutureStudent(models.Model):
    _inherit = 'crm.lead.future.student'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
