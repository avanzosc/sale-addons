# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Picking Return Containers",
    'version': '14.0.1.0.0',
    "author": "Avanzosc",
    "category": "Inventory",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_stock",
        "sale_purchase",
        "stock_move_line_force_done",
    ],
    "data": [
        "views/product_template_view.xml",
        "views/sale_order_line_view.xml",
        "views/purchase_order_view.xml",
        "views/stock_move_line_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
