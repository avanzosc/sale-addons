# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistType(models.Model):
    _name = "product.pricelist.type"
    _description = "Pricelist Type"

    name = fields.Char(string="Name")
