# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    originator_id = fields.Many2one(
        comodel_name='res.company', string='Originator',
        related='product_id.company_id', store=True)
    payer_ids = fields.One2many(
        comodel_name='sale.order.line.payer', string='Payers',
        inverse_name='line_id')
    total_percentage = fields.Float(
        string='Total Percentage', compute='_compute_total_percentage',
        store=True)
    child_id = fields.Many2one(
        comodel_name='res.partner', string='Student',
        related='order_id.child_id')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if not self.payer_ids:
            self.payer_ids = self.sudo().get_payers_info()
        return result

    @api.depends('payer_ids', 'payer_ids.pay_percentage')
    def _compute_total_percentage(self):
        for record in self:
            record.total_percentage = sum(record.mapped(
                'payer_ids.pay_percentage')) if record.payer_ids else 100.0

    @api.multi
    def get_payers_info(self):
        self.ensure_one()
        child = self.order_id.child_id or self.env["res.partner"].browse(
            self.env.context.get("default_child_id"))
        payer_lines = child and child.get_payers_info() or []
        return payer_lines
