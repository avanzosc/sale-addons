# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_categ_id = fields.Many2one(
        string="Product Category", comodel_name="product.category",
        related="product_id.categ_id", store=True, copy=False,
    )
    sequence_to_view = fields.Integer(
        string="Sequence", related="sequence", store=True, copy=False,
    )
    section_line_id = fields.Many2one(
        string="Section line", comodel_name="sale.order.line", copy=False,
    )

    def action_duplicate_line(self):
        if len(self) > 1:
            raise ValidationError(
                _("You can only duplicate 1 at a time, because then the screen"
                  "must be refreshed."))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_shorcut_line.wiz_duplicate_sale_line_action")
        return action

    def action_change_sequence(self):
        if len(self) > 1:
            raise ValidationError(
                _("You can only modify 1 sequence, because then the screen"
                  "must be refreshed."))
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_shorcut_line.wiz_change_sequence_in_sale_line_action")
        return action
