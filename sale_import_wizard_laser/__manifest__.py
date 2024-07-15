# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Import Wizard Laser",
    "version": "16.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "depends": [
        "product_attribute_laser",
        "sale_import_wizard",
        "product_dimension",
        "product_logistics_uom",
        "mrp",
    ],
    "data": [
        "data/sale_import_wizard_laser_data.xml",
        "views/uom_uom_views.xml",
        "views/mrp_bom_views.xml",
        "views/product_product_views.xml",
        "views/sale_order_import_views.xml",
        "views/sale_order_import_line_views.xml",
    ],
    "installable": True,
}
