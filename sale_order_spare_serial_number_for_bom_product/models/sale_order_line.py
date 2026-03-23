# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    spare_serial_number_id = fields.Many2one(
        string="Spare serial number", comodel_name="stock.lot", copy=False
    )

    @api.onchange(
        "spare_serial_number_id",
        "order_id",
        "order_id.spare_serial_number_id",
    )
    def onchange_spare_serial_number_id(self):
        dom = [
            ("sale_ok", "=", True),
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.order_id.company_id.id),
        ]

        if self.order_id and self.order_id.spare_serial_number_id:
            self.spare_serial_number_id = self.order_id.spare_serial_number_id

        if self.spare_serial_number_id:
            bom = self.order_id.search_boms_for_allowed_product_ids()
            allowed_ids = bom.bom_line_ids.mapped("product_id").ids if bom else []
            if allowed_ids:
                dom.append(("id", "in", allowed_ids))

                if self.product_id and self.product_id.id not in allowed_ids:
                    self.product_id = False

        return {"domain": {"product_id": dom}}
