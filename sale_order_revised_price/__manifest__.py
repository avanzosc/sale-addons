# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Order Revised Price",
    "summary": "Customization Module",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "depends": [
        "sale",
        "stock",
        "sale_stock",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "installable": True,
}
