# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class BurdenPickingWizard(models.TransientModel):
    _name = "burden.picking.wizard"
    _description = "Wizard when burden picking is created"

    text = fields.Text(
        string="Text",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(BurdenPickingWizard, self).default_get(fields_list)
        res.update(
            {"text": _("It is going to create a burden picking for all these lines.")}
        )
        return res

    def button_create_burden_picking(self):
        self.ensure_one()
        lines = self._context.get("active_ids")
        lines = self.env["sale.order.line"].browse(lines)
        result = lines.action_create_burden_picking()
        return result
