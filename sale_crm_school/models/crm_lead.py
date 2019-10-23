# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def create_sale_order_for_student(self):
        today = fields.Date.context_today(self)
        date_from = today.replace(month=1, day=1)
        next_year = today.year + 1
        date_to = today.replace(year=next_year, month=12, day=31)
        academic_years = self.env['education.academic_year'].search([
            ('date_start', '>=', date_from),
            ('date_end', '<=', date_to),
        ])
        if not academic_years:
            raise Warning(_('There are no valid academic years'))
        sales = self.env['sale.order']
        futures = self.mapped('future_student_ids').filtered(
            lambda l: l.child_id and not l.sale_order_id and
            l.academic_year_id in academic_years)
        if not futures:
            raise Warning(_('There are not future student to register.'))
        for future in futures:
            vals = future.crm_lead_id._get_vals_for_sale_order(future)
            future.sale_order_id = sales.create(vals)
            future.sale_order_id.onchange_sale_order_template_id()
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
        cond = [('school_id', '=', future.school_id.id),
                ('course_id', '=', future.course_id.id)]
        template = self.env['sale.order.template'].search(cond, limit=1)
        vals = {
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'child_id': future.child_id.id,
            'course_id': future.course_id.id,
            'school_id': future.school_id.id,
            'academic_year_id': future.academic_year_id.id,
            'sale_order_template_id': template.id,
        }
        return vals

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
