# © 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def default_commitment_date(self):
        if "params" in self.env.context and "id" in (
            self.env.context["params"]) and "model" in (
                self.env.context["params"]) and (
                    self.env.context["params"]["model"] == "sale.order"):
            order = self.env["sale.order"].search([
                ("id", "=", self.env.context["params"]["id"])])
            return order.expected_date

    category_ids = fields.Many2many(
        comodel_name="res.partner.category",
        column1='partner_id',
        column2='category_id',
        relation="rel_partner_tag",
        string='Tags',
        related="partner_id.category_id",
        store=True)
    commitment_date = fields.Datetime(default=default_commitment_date)

    @api.onchange("expected_date")
    def _onchange_expected_date(self):
        if self.expected_date and not self.commitment_date:
            self.commitment_date = self.expected_date
