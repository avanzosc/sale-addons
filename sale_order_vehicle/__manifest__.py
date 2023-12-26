# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Vehicle",
    "version": "16.0.1.0.0",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "category": "Sales/Sales",
    "depends": [
        "sale",
        "sale_project",
        "sales_team",
        "fleet",
        "project_vehicle",
        "sale_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/fleet_security.xml",
        "views/sale_order_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
