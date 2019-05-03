# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def create_sale_order_for_student(self):
        date_from = "{}-01-01".format(
            fields.Date.from_string(fields.Date.context_today(self)).year)
        date_from = fields.Date.from_string(date_from)
        date_to = "{}-12-31".format(
            int(fields.Date.from_string(fields.Date.context_today(self)).year)
            + 1)
        date_to = fields.Date.from_string(date_to)
        sales = self.env['sale.order']
        for opor in self:
            futures = opor.mapped('future_student_ids').filtered(
                lambda l: l.child_id and not l.sale_order_id and
                l.academic_year_id and
                l.academic_year_id.date_start >= date_from and
                l.academic_year_id.date_end <= date_to)
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
        template_obj = self.env['sale.order.template']
        vals = {'partner_id': self.partner_id.id,
                'opportunity_id': self.id,
                'child_id': future.child_id.id,
                'course_id': future.course_id.id,
                'school_id': future.school_id.id}
        if future.academic_year_id:
            vals['academic_year_id'] = future.academic_year_id.id
        cond = [('course_id', '=', future.course_id.id),
                ('school_id', '=', future.school_id.id)]
        template = template_obj.search(cond, limit=1)
        if not template:
            cond = [('course_id', '=', future.course_id.id)]
            template = template_obj.search(cond, limit=1)
        if template:
            vals['sale_order_template_id'] = template.id
        return vals

    @api.multi
    def _put_payer_information_in_sale_order(self, future, sale):
        for line in sale.order_line:
            vals = {}
            if line.product_id.categ_id.originator_id:
                vals['originator_id'] = (
                    line.product_id.categ_id.originator_id)
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
