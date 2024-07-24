# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _delivery_carrier_from_sale_import_wizard(self, carrier_id):
        wizard_obj = self.env["choose.delivery.carrier"]
        vals = {
            "order_id": self.id,
            "partner_id": self.partner_id.id,
            "carrier_id": carrier_id.id,
        }
        wizard = wizard_obj.new(vals)
        for comp_onchange in wizard._onchange_methods[
            "carrier_id", "order_id", "partner_id"
        ]:
            comp_onchange(wizard)
        vals = wizard._convert_to_write(wizard._cache)
        new_wizard = wizard_obj.create(vals)
        if new_wizard.delivery_type not in ("fixed", "base_on_rule"):
            new_wizard._get_shipment_rate()
        new_wizard.button_confirm()
