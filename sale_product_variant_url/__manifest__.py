# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Variant URL - Sale Glue",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Show Product URL in Sale Order Reports if both modules are installed",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente<alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "sale",
        "product_variant_url",
    ],
    "data": ["views/sale_report_template.xml"],
    "installable": True,
    "auto_install": True,
}
