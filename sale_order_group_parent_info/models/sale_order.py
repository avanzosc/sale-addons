# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    main_parent_id = fields.Many2one(
        string="Main Partner",
        comodel_name="res.partner",
        related="partner_id.commercial_partner_id",
        store=True,
        copy=False,
    )
    main_state_id = fields.Many2one(
        string="Main Province",
        comodel_name="res.country.state",
        compute="_compute_main_state_id",
        store=True,
        copy=False,
    )

    @api.depends("main_parent_id", "main_parent_id.state_id")
    def _compute_main_state_id(self):
        for sale in self:
            sale.main_state_id = (
                sale.main_parent_id.state_id.id
                if sale.main_parent_id.state_id
                else False
            )
