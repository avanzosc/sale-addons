# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import Warning


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
        sales = self.env['sale.order'].search([
            ('academic_year_id', 'in', academic_years.ids),
            ('state', 'in', ['draft', 'sent']),
        ])
        for opor in self:
            futures = opor.mapped('future_student_ids').filtered(
                lambda l: l.child_id and not l.sale_order_id and
                l.academic_year_id in academic_years)
            for future in futures:
                vals = opor._get_vals_for_sale_order(future)
                sale = self.env['sale.order'].create(vals)
                sale.onchange_sale_order_template_id()
                future.sale_order_id = sale.id
                future.child_id.educational_category = 'student'
                opor._put_payer_information_in_sale_order(future, sale)
                sales += sale
        return {'name': _('Sale orders'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'sale.order',
                'domain': [('id', 'in', sales.ids)]}

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
                vals2.append((0, 0,
                              {'payer_id': payer.responsible_id.id,
                               'pay_percentage': payer.payment_percentage}))
            if vals2:
                vals['payer_ids'] = vals2
            line.write(vals)


class CrmLeadFutureStudent(models.Model):
    _inherit = 'crm.lead.future.student'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
