# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Student Event",
    'version': '14.0.1.1.0',
    "author": "Avanzosc",
    "category": "Sales",
    "depends": [
        "sale_order_line_menu",
        "education_center",
        "event",
        "event_sale",
        "event_schedule"
    ],
    "data": [
        "views/assets.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "views/event_event_ticket_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
