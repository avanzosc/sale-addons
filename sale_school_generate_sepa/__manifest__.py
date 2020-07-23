# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale School Generate Sepa",
    "version": "12.0.1.3.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_school",
        "account_banking_mandate",
        "account_banking_sepa_direct_debit",
        "account_banking_mandate_usability",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,
}
