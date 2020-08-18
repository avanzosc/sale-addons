# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    type_id = fields.Many2one(
        comodel_name="product.pricelist.type", string="Pricelist Type")
    child_num = fields.Integer(
        string="Child Number",
        help="This field defines the child position over enrollees from the "
             "same family")
