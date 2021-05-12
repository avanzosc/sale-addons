# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner')
    education_center_id = fields.Many2one(
        string='Education center', related='student_id.education_center_id',
        comodel_name='res.partner', store=True)
    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
    is_member = fields.Boolean(string='Is member?', default=False)

    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.event_id:
            line = self.event_id.mapped("event_ticket_ids").filtered(
                lambda x: x.is_member == self.is_member and
                x.product_id == self.product_id)
            if line and len(line) == 1:
                self.price_unit = line.price
                result['price_unit'] = line.price
        return result

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        result = super(SaleOrderLine, self).product_uom_change()
        if self.product_id and self.event_id:
            line = self.event_id.mapped("event_ticket_ids").filtered(
                lambda x: x.is_member == self.is_member and
                x.product_id == self.product_id)
            if line and len(line) == 1:
                self.price_unit = line.price
        return result

    @api.onchange("event_id", "is_member")
    def _onchange_event_is_member(self):
        domain = {}
        if not self.event_id:
            domain['product_id'] = [
                ('sale_ok', '=', True), '|', ('company_id', '=', False),
                ('company_id', '=', self.env.user.company_id.id)]
        if self.event_id:
            line = self.event_id.mapped("event_ticket_ids").filtered(
                lambda x: x.is_member == self.is_member)
            if line:
                domain['product_id'] = [
                    ('id', 'in', line.mapped('product_id').ids),
                    ('sale_ok', '=', True), '|', ('company_id', '=', False),
                    ('company_id', '=', self.env.user.company_id.id)]
            if line and len(line) == 1:
                self.product_id = line.product_id.id
                self.price_unit = line.price
        return {'domain': domain}
