# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False):
        res = super(SaleOrder, self)._create_invoices(
            grouped=grouped, final=final)
        self.mapped("order_line")._create_multiple_hour_invoice_line()
        return res
