# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from .common import TestSaleSchoolGenerateSepaCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleSchoolGenerateSepa(TestSaleSchoolGenerateSepaCommon):

    def test_sale_school_generate_sepa(self):
        self.assertFalse(self.sale_order.sepa_count)
        self.sale_order.action_confirm()
        self.assertEquals(self.sale_order.sepa_count, 1)
        action_dict = self.sale_order.action_view_sepa_from_sale_order()
        mandates = self.sale_order._find_payer_mandates()
        self.assertIn(('id', 'in', mandates.ids),
                      action_dict.get("domain"))
        for mandate in mandates:
            self.assertEquals(mandate.format, "sepa")
            self.assertEquals(mandate.type, "recurrent")
            self.assertEquals(mandate.scheme, "CORE")
            self.assertTrue(mandate.signature_date)
            self.assertEquals(mandate.state, "valid")

    def test_sale_school_generate_sepa2(self):
        mandate_wiz = self.env["res.partner.bank.mandate.generator"].create({
            "bank_ids": [(6, 0, self.bank.ids)],
            "mandate_format": "sepa",
            "mandate_type": "recurrent",
            "mandate_scheme": "CORE",
            "mandate_recurrent_sequence_type": "recurring",
        })
        mandate_wiz.button_generate_mandates()
        self.assertEquals(self.sale_order.sepa_count, 1)
        for mandate in self.sale_order._find_payer_mandates():
            self.assertFalse(mandate.signature_date)
            self.assertEquals(mandate.state, "draft")
        self.sale_order.action_confirm()
        self.assertEquals(self.sale_order.sepa_count, 1)
        for mandate in self.sale_order._find_payer_mandates():
            self.assertTrue(mandate.signature_date)
            self.assertEquals(mandate.state, "valid")
