# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Penalty Warning",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "author": "https://avanzosc.es/",
    "license": "AGPL-3",
    "depends": [
        "base_penalty_warning",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/penalty_warning_views.xml",
        "views/sale_order_views.xml",
    ],
}
