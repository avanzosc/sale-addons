# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Custom Sequence",
    "version": "18.0.1.0.0",
    "category": "Sales/Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/sale-addons",
    "depends": [
        "sale",
    ],
    "data": [
        "data/ir_sequence_data.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_install_calculate_customized_sequence",
}
