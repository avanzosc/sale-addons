# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestSaleTemplatePriceUpdateCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleTemplatePriceUpdateCommon, cls).setUpClass()
        cls.tmpl_line_model = cls.env["sale.order.template.line"]
        cls.tmpl_option_model = cls.env["sale.order.template.option"]
        cls.settings = cls.env["res.config.settings"].create({})
        cls.start_price = 10.0
        cls.end_price = 20.0
        cls.product = cls.env["product.product"].create({
            "name": "Test Product",
            "price": cls.start_price,
        })
        cls.template = cls.env["sale.order.template"].create({
            "name": "Test Template Order",
        })
        new_template_line = cls.tmpl_line_model.new({
            "sale_order_template_id": cls.template.id,
            "product_id": cls.product.id,
        })
        new_template_line._onchange_product_id()
        tmpl_line_vals = new_template_line._convert_to_write(
            new_template_line._cache)
        cls.template_line = cls.tmpl_line_model.create(tmpl_line_vals)
        new_template_option = cls.tmpl_option_model.new({
            "sale_order_template_id": cls.template.id,
            "product_id": cls.product.id,
        })
        new_template_option._onchange_product_id()
        tmpl_option_vals = new_template_option._convert_to_write(
            new_template_option._cache)
        cls.template_option = cls.tmpl_option_model.create(tmpl_option_vals)
