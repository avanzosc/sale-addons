# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_category_ids = fields.Many2many(
        string="Customer categories", comodel_name="res.partner.category",
        related="partner_id.category_id", relation="rel_saleorder_partner_cat",
        column1="sale_id", column2="cat_id",copy=False, store=True)
