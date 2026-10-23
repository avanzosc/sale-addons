# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CatalogProductXlsx(models.AbstractModel):
    _name = "report.catalog.product_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Catalog Products Price Report"

    def generate_xlsx_report(self, workbook, data, objects):
        partner_id = data.get("partner_id", None)
        partner = None
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
        table_header = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "fg_color": "#D7E4BC",
            }
        )
        table_header.set_text_wrap()
        table_detail_right_num = workbook.add_format(
            {
                "border": 1,
                "align": "right",
                "valign": "vcenter",
            }
        )
        table_detail_right_num.set_num_format("#,##0.00")
        for catalog in objects:
            worksheet = workbook.add_worksheet(catalog.display_name)
            worksheet.write(0, 0, "Product", table_header)
            worksheet.write(0, 1, "EAN code", table_header)
            worksheet.write(0, 2, "Product reference", table_header)
            worksheet.write(0, 3, "Brand", table_header)
            worksheet.write(0, 4, "Product category", table_header)
            worksheet.write(0, 5, "Delivery date start", table_header)
            worksheet.write(0, 6, "Delivery date end", table_header)
            worksheet.write(0, 7, "Price", table_header)
            worksheet.write(0, 8, "RRP", table_header)
            worksheet.write(0, 9, "B2B stock", table_header)
            all_attributes = catalog.mapped(
                "product_tmpl_ids.attribute_line_ids.attribute_id"
            )
            n = 10
            for attribute in all_attributes:
                worksheet.write(0, n, attribute.display_name, table_header)
                n = n + 1

            # Order Lines
            n = 1
            for product in catalog.mapped("product_tmpl_ids.product_variant_ids"):
                product_pricelist_item = self.with_company(
                    catalog.company_id
                ).get_product_pricelist_item(product, catalog, partner)
                if product_pricelist_item:
                    worksheet.write(n, 0, product.name)
                    worksheet.write(n, 1, product.barcode)
                    worksheet.write(n, 2, product.default_code)
                    worksheet.write(n, 3, product.product_brand_id.name)
                    worksheet.write(n, 4, product.categ_id.display_name)
                    if product_pricelist_item.date_start:
                        worksheet.write(
                            n,
                            5,
                            fields.Date.to_string(product_pricelist_item.date_start)
                            or "",
                        )
                    if product_pricelist_item.date_end:
                        worksheet.write(
                            n,
                            6,
                            fields.Date.to_string(product_pricelist_item.date_end)
                            or "",
                        )
                    worksheet.write(
                        n,
                        7,
                        product_pricelist_item.fixed_price
                        if product_pricelist_item
                        else product.lst_price,
                    )
                    try:
                        pvp_price = (
                            product_pricelist_item.pvp_price
                            if product_pricelist_item
                            else product.list_price_tax
                        )
                    except Exception:
                        pvp_price = product.list_price_tax
                    worksheet.write(n, 8, pvp_price)
                    try:
                        virtual_available = product.with_company(
                            catalog.company_id
                        ).b2b_virtual_available
                    except Exception:
                        virtual_available = product.with_company(
                            catalog.company_id
                        ).virtual_available
                    worksheet.write(
                        n,
                        9,
                        virtual_available,
                    )
                    c = 10
                    for attribute in all_attributes:
                        if (
                            attribute.id
                            in product.product_template_attribute_value_ids.mapped(
                                "attribute_id"
                            ).ids
                        ):
                            attrib_val = (
                                product.product_template_attribute_value_ids.filtered(
                                    lambda a, attr=attribute: a.attribute_id == attr
                                )
                            )
                            name = attrib_val.name
                            worksheet.write(n, c, name)
                        c = c + 1
                    n = n + 1

    def get_product_pricelist_item(self, product, catalog, partner=None):
        if not partner:
            return None

        if catalog:
            partner = partner.with_company(catalog.company_id)

        if catalog and catalog.commitment_date:
            force_pricelist_date = catalog.commitment_date.date()
        else:
            force_pricelist_date = datetime.today().date()

        pricelist = partner.property_product_pricelist
        base_pricelists = pricelist.item_ids.mapped("base_pricelist_id")
        if base_pricelists:
            pricelist = base_pricelists[:1]

        product_context = dict(force_pricelist_date=force_pricelist_date)
        price, rule_id = pricelist.with_context(
            **product_context
        )._get_product_price_rule(product, 1.0, partner)
        pricelist_item = self.env["product.pricelist.item"].browse(rule_id)
        return pricelist_item
