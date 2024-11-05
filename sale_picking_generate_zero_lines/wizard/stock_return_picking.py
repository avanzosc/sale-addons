# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.model
    def default_get(self, fields):
        result = super(StockReturnPicking, self).default_get(fields)
        if (
            self.env.context.get("active_id")
            and self.env.context.get("active_model") == "sale.order"
        ):
            sale = self.env["sale.order"].browse(self.env.context.get("active_id"))
            if sale.exists():
                done_pickings = sale.picking_ids.filtered(lambda c: c.state == "done")
                if len(sale.picking_ids) != 1:
                    raise ValidationError(
                        _("You may only return one picking at a time.")
                    )
                elif not done_pickings:
                    raise ValidationError(_("The picking is not done."))
                else:
                    result.update({"picking_id": done_pickings.id})
        return result
