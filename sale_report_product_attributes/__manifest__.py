# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Report Product Attributes",
    "version": "18.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "category": "Sale",
    "depends": [
        "acysos_hlc",
        "product",
        "report_xlsx",
        "sale",
        "sales_team",
    ],
    "data": [
        "reports/product_attribute_sale_report.xml",
        "reports/product_attribute_catalog_report.xml",
        "reports/catalog_product_xlsx_report_xlsx_report_view.xml",
        "wizards/open_sale_product_attributes_report_view.xml",
        "wizards/catalog_product_export_xlsx_report_view.xml",
        "views/views.xml",
        "security/ir.model.access.csv",
    ],
    "license": "AGPL-3",
    "installable": True,
}
