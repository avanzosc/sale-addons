# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    spare_serial_number_id = fields.Many2one(
        string="Spare serial number", comodel_name="stock.production.lot", copy=False
    )

    @api.onchange("spare_serial_number_id")
    def onchange_spare_serial_number_id(self):
        for line in self:
            if not line.spare_serial_number_id:
                domain = {
                    "domain": {
                        "product_id": [
                            ("sale_ok", "=", True),
                            "|",
                            ("company_id", "=", False),
                            ("company_id", "=", line.order_id.company_id),
                        ]
                    }
                }
            else:
                domain = {
                    "domain": {
                        "product_id": [
                            ("id", "in", line.order_id.allowed_product_ids.ids),
                            ("sale_ok", "=", True),
                            "|",
                            ("company_id", "=", False),
                            ("company_id", "=", line.order_id.company_id),
                            ("id", "in", line.order_id.allowed_product_ids.ids),
                        ]
                    }
                }
        return domain
