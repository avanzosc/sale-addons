# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields
from odoo.tests import common


class TestSaleOrderLineContractHeadquarter(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineContractHeadquarter, cls).setUpClass()
        cls.sale_obj = cls.env["sale.order"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.invoice_obj = cls.env["account.move"]
        cls.company = cls.env["res.company"]._company_default_get("sale.order")
        vals = {
            "name": "User event headquarter",
            "login": "evenheadquartner@avanzosc.es",
        }
        cls.user = cls.env["res.users"].create(vals)
        cls.user.partner_id.write(
            {"parent_id": cls.company.partner_id.id, "headquarter": True}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner sale order line contract headquarter ",
                "user_id": cls.env.ref("base.user_admin").id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product sale order line contract headquarter",
                "default_code": "Psolchq",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "recurring_rule_type": "monthly",
                "recurring_interval": 1,
            }
        )
        sale_line_vals = {
            "product_id": cls.product.id,
            "name": cls.product.name,
            "product_uom_qty": 1,
            "product_uom": cls.product.uom_id.id,
            "price_unit": 100,
        }
        sale_vals = {
            "headquarter_id": cls.user.partner_id.id,
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)],
        }
        cls.sale1 = cls.sale_obj.create(sale_vals)
        cond = [
            ("partner_id", "=", cls.sale1.partner_id.id),
            ("contract_type", "=", "sale"),
        ]
        contracts = cls.env["contract.contract"].search(cond)
        contracts.unlink()

    def test_sale_order_line_contract_headquarter(self):
        self.sale1._action_confirm()
        self.assertEqual(self.sale1.count_contracts, 1)
        self.assertEqual(len(self.sale1.contract_ids[0].contract_line_ids), 1)
        self.assertEqual(len(self.sale1.contract_ids), 1)
        for contract in self.sale1.contract_ids:
            self.assertEqual(contract.headquarter_id, self.user.partner_id)
            contract.contract_line_fixed_ids.write(
                {
                    "date_start": fields.Date.today(),
                    "next_period_date_start": fields.Date.today(),
                    "recurring_next_date": fields.Date.today(),
                }
            )
            contract.recurring_create_invoice()
            cond = [("invoice_origin", "=", contract.name)]
            invoice = self.invoice_obj.search(cond, limit=1)
            self.assertEqual(invoice.headquarter_id, contract.headquarter_id)
