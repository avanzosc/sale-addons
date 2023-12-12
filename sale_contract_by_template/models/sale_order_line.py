# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

# EL MODULO contract_sale_generation crea un campo llamado contract_line_id en las
# líneas de pedido, pero el funcionamiento es a la inversa de lo que queremos.
# Así que hay que recordar no llamarlo igual, por si acaso.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    contract_ids = fields.One2many(
        comodel_name="contract.contract",
        inverse_name="sale_line_id",
        string="Contracts",
    )

    # no trigger product_id.invoice_policy to avoid retroactively changing SO
    @api.depends("qty_invoiced", "qty_delivered", "product_uom_qty", "order_id.state")
    def _get_to_invoice_qty(self):
        super()._get_to_invoice_qty()
        for line in self:
            if line.product_id.contract_tmpl_id:
                line.qty_to_invoice = 0

    def _prepare_contract(self):
        self.ensure_one()
        contract = self.env["contract.contract"].new(
            {
                "contract_type": "sale",
                "name": self.display_name,
                "partner_id": self.order_partner_id.id,
                "invoice_partner_id": self.order_id.partner_invoice_id.id,
                "company_id": self.company_id.id,
                "user_id": self.salesman_id.id,
                "contract_template_id": self.product_id.contract_tmpl_id.id,
                "sale_line_id": self.id,
                "line_recurrence": True,
            }
        )
        contract._onchange_partner_id()
        if self.order_id.partner_invoice_id:
            contract.invoice_partner_id = self.order_id.partner_invoice_id.id
        if self.order_id.pricelist_id:
            contract.pricelist_id = (self.order_id.pricelist_id.id,)
        if self.order_id.payment_term_id:
            contract.payment_term_id = self.order_id.payment_term_id.id
        if self.order_id.fiscal_position_id:
            contract.fiscal_position_id = self.order_id.fiscal_position_id.id
        # Get other contract values from template onchange
        contract._onchange_contract_template_id()
        return contract._convert_to_write(contract._cache)

    def _prepare_contract_values(self):
        contracts_values = []
        for sale_line in self:
            for _cnt in range(int(sale_line.product_uom_qty)):
                contracts_values.append(sale_line._prepare_contract())
        return contracts_values

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if line.state == "sale" and line.product_id.contract_tmpl_id:
                line.sudo()._contract_generation()
        return lines

    def _contract_generation(self):
        contract_values = self._prepare_contract_values()
        contracts = self.env["contract.contract"].create(contract_values)
        return contracts
