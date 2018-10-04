# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_price = fields.Float(
        string='Product Price', related='product_id.lst_price', store=True,
        readonly=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_return_confirm = fields.Boolean(
        string='Stock return', help="Check this field if the carrier has "
        "confirmed the picking of the material to return")
