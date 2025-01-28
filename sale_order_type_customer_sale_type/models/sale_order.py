# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("partner_id", "company_id")
    def _compute_sale_type_id(self):
        super(SaleOrder, self)._compute_sale_type_id()
        for record in self:
            sale_type = (
                record.partner_id.with_company(record.company_id).sale_type
                or record.partner_id.commercial_partner_id.with_company(
                    record.company_id
                ).sale_type
            )
            # Default user sale type value
            if not sale_type:
                sale_type = record.default_get(["type_id"]).get("type_id", False)
            # Get first sale type value
            if not sale_type:
                sale_type = False
            if not sale_type:
                record.type_id = sale_type
