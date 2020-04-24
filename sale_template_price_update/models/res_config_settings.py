# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    automatic_price_update = fields.Boolean(
        string="Update Quotation Template Prices",
        help="If this check is marked it will update the prices in the related"
             " quotation templates")

    @api.model
    def get_values(self):
        res = super(SaleConfigSettings, self).get_values()
        get_param = self.env["ir.config_parameter"].sudo().get_param
        # the value of the parameter is a nonempty string
        res.update(
            automatic_price_update=get_param(
                "sale.automatic_price_update", "False").lower() == "true",
        )
        return res

    @api.multi
    def set_values(self):
        super(SaleConfigSettings, self).set_values()
        set_param = self.env["ir.config_parameter"].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param("sale.automatic_price_update",
                  repr(self.automatic_price_update))
