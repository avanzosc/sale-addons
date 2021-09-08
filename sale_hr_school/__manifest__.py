# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sales for School - HR extension",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "sale_school",
        "hr_school",
    ],
    "excludes": [],
    "data": [
        "views/sale_order_view.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
