# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    section_to_print_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id', string='Sections to print',
        domain=[('display_type', '=', 'line_section')])

    def _compute_line_data_for_template_change(self, line):
        data = super(
            SaleOrder, self)._compute_line_data_for_template_change(line)
        data.update({'print_section_lines': line.print_section_lines,
                     'sequence': line.my_sequence})
        return data

    def calculate_recalculate_to_print(self):
        for section in self.section_to_print_ids:
            salelines = self.mapped('order_line').filtered(
                lambda x: x.sequence >= section.my_sequence and not
                x.display_type)
            if salelines:
                salelines.with_context(update_print=True).write(
                    {'print_section_lines':
                     section.print_section_lines})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    print_section_lines = fields.Boolean(
        string='Print section lines', default=True)
    my_sequence = fields.Integer(string='My sequence', related='sequence')

    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        line.order_id.calculate_recalculate_to_print()
        return line

    @api.multi
    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        lines = self.filtered(lambda x: x.display_type == 'line_section')
        if 'update_print'not in self.env.context and ('sequence' in vals):
            for line in self:
                line.order_id.calculate_recalculate_to_print()
        if ('update_print'not in self.env.context and
           'print_section_lines' in vals):
            for line in lines:
                line.order_id.calculate_recalculate_to_print()
        return result
