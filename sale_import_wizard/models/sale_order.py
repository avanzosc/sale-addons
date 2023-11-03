# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_import_id = fields.Many2one(
        string="", comodel_name="sale.order.import", copy=False,
        readonly="1")
    total_amount_from_import = fields.Float(
        string="Total amount from import", readonly="1", copy=False)
    different_amounts = fields.Boolean(
        string="Different import and total untaxed amounts",
        compute="_compute_different_amounts", store=True, copy=False)

    @api.depends("total_amount_from_import", "amount_untaxed")
    def _compute_different_amounts(self):
        for sale in self:
            different_amounts = False
            if (sale.total_amount_from_import > 0 and
                sale.amount_untaxed > 0 and
                    sale.total_amount_from_import != sale.amount_untaxed):
                different_amounts = True
            sale.different_amounts = different_amounts
