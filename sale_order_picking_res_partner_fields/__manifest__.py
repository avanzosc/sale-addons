{
    "name": "Sale Order Picking Res Partner Fields",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "depends": ["sale_management", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
