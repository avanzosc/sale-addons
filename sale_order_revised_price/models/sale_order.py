# -*- coding: utf-8 -*-
# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    revised_price = fields.Boolean(
        string="Revised price", default=False, copy=False
    )
