# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Product Catalog Upload to FTP",
    "summary": "Upload Product Catalog to FTP",
    "version": "18.0.1.0.0",
    "category": "Hidden",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "depends": [
        "sale_product_catalog",
    ],
    "data": [
        "data/product_catalog_ftp_data.xml",
        "security/product_catalog_ftp_rules.xml",
        "security/ir.model.access.csv",
        "views/product_catalog_ftp_views.xml",
        "views/product_catalog_views.xml",
    ],
    "installable": True,
}
