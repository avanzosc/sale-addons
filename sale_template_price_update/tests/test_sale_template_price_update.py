# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestSaleTemplatePriceUpdateCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleTemplatePriceUpdate(TestSaleTemplatePriceUpdateCommon):

    def test_price_update_product_product(self):
        self.settings.automatic_price_update = 'True'
        self.settings.set_values()
        self.assertEquals(self.template_line.price_unit, self.start_price)
        self.assertEquals(self.template_option.price_unit, self.start_price)
        self.product.write({
            "lst_price": self.end_price,
        })
        self.assertEquals(self.template_line.price_unit, self.end_price)
        self.assertEquals(self.template_option.price_unit, self.end_price)

    def test_price_update_product_template(self):
        self.settings.automatic_price_update = 'True'
        self.settings.set_values()
        self.assertEquals(self.template_line.price_unit, self.start_price)
        self.assertEquals(self.template_option.price_unit, self.start_price)
        self.product.product_tmpl_id.write({
            "list_price": self.end_price,
        })
        self.assertEquals(self.template_line.price_unit, self.end_price)
        self.assertEquals(self.template_option.price_unit, self.end_price)

    def test_template_price_update(self):
        self.assertFalse(self.settings.automatic_price_update)
        self.assertEquals(self.template_line.price_unit, self.start_price)
        self.assertEquals(self.template_option.price_unit, self.start_price)
        self.product.product_tmpl_id.write({
            "list_price": self.end_price,
        })
        self.assertNotEquals(self.template_line.price_unit, self.end_price)
        self.assertNotEquals(self.template_option.price_unit, self.end_price)
        self.template.update_price()
        self.assertEquals(self.template_line.price_unit, self.end_price)
        self.assertEquals(self.template_option.price_unit, self.end_price)

    def test_res_config(self):
        """Test the config file"""
        self.assertFalse(self.settings.automatic_price_update)
        self.settings.automatic_price_update = 'True'
        self.settings.set_values()
        self.assertTrue(self.settings.automatic_price_update)
