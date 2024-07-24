# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderImport(models.Model):
    _inherit = "sale.order.import"

    carrier_id = fields.Many2one(
        string="Shipping Method",
        comodel_name="delivery.carrier",
        help="Choose the method to deliver your goods",
        copy=False,
    )

    def action_process(self):
        result = super(SaleOrderImport, self).action_process()
        orders = self.mapped("import_line_ids.sale_order_id")
        if self.carrier_id:
            for sale in orders:
                sale._delivery_carrier_from_sale_import_wizard(self.carrier_id)
        return result
