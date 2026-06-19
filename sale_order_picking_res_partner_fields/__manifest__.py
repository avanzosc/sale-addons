{
    "name": "Sale Order Picking Res Partner Fields",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Adds delivery and installation fields in sales orders and pickings",
    "author": "Avanzosc",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "depends": ["sale_management", "sale_stock"],
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
