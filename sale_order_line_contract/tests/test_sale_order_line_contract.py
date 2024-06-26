# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestSaleOrderLineContract(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineContract, cls).setUpClass()
        cls.sale_obj = cls.env["sale.order"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.company = cls.env["res.company"]._company_default_get("sale.order")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner sale order line contract",
                "user_id": cls.env.ref("base.user_admin").id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product sale order line contract",
                "default_code": "Psolc",
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
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)],
        }
        cls.sale1 = cls.sale_obj.create(sale_vals)

    def test_sale_order_line_contract(self):
        self.sale1._action_confirm()
        self.assertEquals(self.sale1.count_contracts, 1)
        self.assertEquals(len(self.sale1.contract_ids[0].contract_line_ids), 1)
        sale_line_vals = {
            "product_id": self.product.id,
            "name": self.product.name,
            "product_uom_qty": 1,
            "product_uom": self.product.uom_id.id,
            "price_unit": 100,
        }
        sale_vals = {
            "partner_id": self.partner.id,
            "partner_invoice_id": self.partner.id,
            "partner_shipping_id": self.partner.id,
            "company_id": self.company.id,
            "order_line": [(0, 0, sale_line_vals)],
        }
        sale2 = self.sale_obj.create(sale_vals)
        sale2._action_confirm()
        self.assertEquals(sale2.count_contracts, 1)
        self.assertEquals(len(sale2.contract_ids[0].contract_line_ids), 2)
        result = sale2.action_view_contracts()
        domain = [
            "&",
            ("id", "in", sale2.contract_ids[0].ids),
            ("contract_type", "=", "sale"),
        ]
        self.assertEquals(result.get("domain"), domain)
