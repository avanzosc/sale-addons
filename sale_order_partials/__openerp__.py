# -*- coding: utf-8 -*-
# © Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Partial sale orders",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "stock",
        "sale_order_type",
    ],
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Odoo Community Association (OCA)",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Mikel Arregi <mikelarregi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "",
    "summary": "",
    "data": [
        "views/sale_order_view.xml",
        "views/res_config_view.xml",
        "wizard/duplicate_upgradable_sale_view.xml",
    ],
    "installable": True,
}
