# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "order_id, sequence_to_view, id"

    sale_order_space_id = fields.Many2one(
        string="Sale Order Space", comodel_name="sale.order.space",
        copy=False,
    )
    space_sequence = fields.Integer(
        string="Space Sequence", related="sale_order_space_id.sequence",
        store=True, copy=False, readonly=True,
    )
    sale_order_template_line_sequence = fields.Integer(
        string="Template Line Sequence", default=0, copy=False
    )
    sequence_to_view = fields.Char(
        string="Sequence to view", compute="_compute_sequence_to_view", store=True,
        related=False, copy=False,
    )

    @api.depends("space_sequence", "sale_order_template_line_sequence",
                 "sequence")
    def _compute_sequence_to_view(self):
        for line in self:
            line_sequence = (
                line.sequence if line.sequence >= 0 else line.sequence * -1)
            sequence_to_view = "{}{}{}".format(
                str(line.space_sequence).zfill(2),
                str(line.sale_order_template_line_sequence).zfill(3),
                line_sequence)
            line.sequence_to_view = sequence_to_view

    def action_duplicate_line(self):
        if len(self) > 1:
            raise ValidationError(
                _("You can only duplicate 1 at a time, because then the screen"
                  "must be refreshed."))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_template_space.wiz_duplicate_sale_line_action")
        return action
