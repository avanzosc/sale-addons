# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common


class SaleServiceMultiplePrice(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sale_obj = cls.env["sale.order"]
        timesheet_obj = cls.env["account.analytic.line"]
        service_product = cls.env["product.product"].create({
            "name": "Service Product",
            "type": "service",
            "lst_price": 10.0,
            "service_type": "timesheet",
            "service_policy": "delivered_timesheet",
            "service_tracking": "task_in_project",
        })
        cls.sale_order = sale_obj.create({
            "partner_id": 1,
            "order_line": [(0, 0, {
                "product_id": service_product.id,
                "price_unit": service_product.lst_price,
                "multiple_price_unit": service_product.lst_price / 2.0,
            })],
        })
        cls.sale_order.action_confirm()
        cls.unit_amount = 2.5
        cls.amount = (cls.unit_amount * service_product.lst_price * -1)
        cls.timesheet_count = 3
        for task in cls.sale_order.tasks_ids:
            for i in range(0, cls.timesheet_count):
                task.write({
                    "timesheet_ids": [(0, 0, {
                        "name": "Timesheet Test {}".format(i),
                        "unit_amount": cls.unit_amount,
                        "amount": cls.amount,
                        "account_id": task.project_id.analytic_account_id.id,
                        "project_id": task.project_id.id,
                    })]
                })
