# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def inter_company_create_sale_order(self, company):
        for order in self:
            intercompany_uid = (
                company.intercompany_user_id
                and company.intercompany_user_id.id
                or False
            )
            company_partner = order.company_id.partner_id.with_user(intercompany_uid)
            if company_partner != order.partner_id:
                return super().inter_company_create_sale_order(company=company)
