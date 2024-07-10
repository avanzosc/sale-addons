# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Compute Planned Hours on Tasks Module",
    "summary": "Module to compute initial planned hours on tasks based on sale order lines",
    "website": "https://github.com/avanzosc/sale-addons",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "version": "14.0.1.0.0",
    "depends": ["sale_project"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
