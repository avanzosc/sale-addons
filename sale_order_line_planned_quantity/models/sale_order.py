# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    difference_between_ordered_planned = fields.Boolean(
        string="Difference Between Ordered And Planned",
        store=True,
        copy=False,
        compute="_compute_planned_quantity",
    )

    @api.depends(
        "order_line",
        "order_line.difference_between_ordered_planned",
    )
    def _compute_planned_quantity(self):
        for sale in self:
            sale.difference_between_ordered_planned = any(
                [x.difference_between_ordered_planned for x in sale.order_line]
            )
