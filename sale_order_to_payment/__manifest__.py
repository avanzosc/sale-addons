# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order To Payment",
    "version": "14.0.1.0.0",
    "category": "Analytic",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "account",
        "sale",
        "account_move_to_payment",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
