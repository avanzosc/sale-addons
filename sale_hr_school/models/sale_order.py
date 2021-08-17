# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    teacher_id = fields.Many2one(
        comodel_name="hr.employee", string="Teacher",
        readonly=True, states={'draft': [('readonly', False)]},)

    @api.multi
    def get_supervising_teacher(self):
        self.ensure_one()
        supervising_teacher = self.env[
            "hr.employee.supervised.year"].get_supervised(
                self.child_id, self.academic_year_id)
        if supervising_teacher:
            self.write({
                "teacher_id": supervising_teacher.teacher_id.id,
            })
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        supervising_obj = self.env["hr.employee.supervised.year"]
        for sale in self.filtered("teacher_id"):
            supervising_obj._find_or_create_supervised(
                sale.child_id, sale.academic_year_id, sale.teacher_id)
        return res

    @api.multi
    def action_cancel(self):
        supervised_obj = self.env["hr.employee.supervised.year"]
        for order in self:
            supervising_teacher = supervised_obj.get_supervised(
                order.child_id, order.academic_year_id)
            supervising_teacher.unlink()
        return super(SaleOrder, self).action_cancel()
