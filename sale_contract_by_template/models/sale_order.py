# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_count = fields.Integer(
        string="Contract Count",
        compute="_compute_contract_id",
        readonly=True,
    )
    contract_ids = fields.Many2many(
        comodel_name="contract.contract",
        string="Contracts",
        compute="_compute_contract_id",
        readonly=True,
        copy=False,
    )

    @api.depends("order_line.contract_ids")
    def _compute_contract_id(self):
        for order in self:
            contracts = order.mapped("order_line.contract_ids")
            order.contract_ids = contracts
            order.contract_count = len(contracts)

    def action_view_contract(self):
        contracts = self.mapped("contract_ids")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "contract.action_customer_contract"
        )
        if len(contracts) > 1:
            action["domain"] = [("id", "in", contracts.ids)]
        elif len(contracts) == 1:
            form_view = [
                (
                    self.env.ref("contract.contract_contract_customer_form_view").id,
                    "form",
                )
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = contracts.id
        else:
            action = {"type": "ir.actions.act_window_close"}

        context = {}
        if len(self) == 1:
            context.update(
                {
                    "default_partner_id": self.partner_id.id,
                    "default_user_id": self.user_id.id,
                }
            )
        action["context"] = context
        return action

    def _action_confirm(self):
        """On SO confirmation, some lines should generate a contract."""
        result = super()._action_confirm()
        if len(self.company_id) == 1:
            # All orders are in the same company
            self.order_line.sudo()._contract_generation()
        return result
