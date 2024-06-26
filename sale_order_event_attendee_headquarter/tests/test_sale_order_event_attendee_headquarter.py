# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderEventAttendeeHeadquarter(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderEventAttendeeHeadquarter, cls).setUpClass()
        cls.registration_obj = cls.env["event.registration"]
        cls.sale_payment_obj = cls.env["sale.advance.payment.inv"]
        cls.invoice_obj = cls.env["account.move"]
        cls.product_obj = cls.env["product.product"]
        cls.sale_order_line_obj = cls.env["sale.order.line"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.customer = cls.env.ref("base.res_partner_12")
        cls.resource_calendar = cls.env.ref("resource.resource_calendar_std")
        cls.event_confirmed_stage = cls.env.ref("event.event_stage_announced")
        cls.company = cls.env["res.company"]._company_default_get("sale.order")
        cls.customer.write(
            {"parent_id": cls.company.partner_id.id, "headquarter": True}
        )
        vals = {
            "name": "User sale order event attendee headquarter",
            "login": "usoeah@avanzosc.es",
        }
        user = cls.env["res.users"].create(vals)
        vals = {
            "name": "employee sale order event attendee headquarter",
            "user_id": user.id,
        }
        cls.env["hr.employee"].create(vals)
        cls.product = cls.product_obj.create(
            {
                "name": "product sale order event attendee headquarter",
                "default_code": "PSOEAH",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "type": "consu",
                "invoice_policy": "order",
            }
        )
        cls.product_service = cls.product_obj.create(
            {
                "name": "product service sale order event attendee headquarter",
                "default_code": "PSSOEAH",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "type": "service",
                "invoice_policy": "order",
                "service_policy": "delivered_timesheet",
                "service_tracking": "task_in_project",
            }
        )
        cls.event = cls.env["event.event"].create(
            {
                "name": "Avanzosc sale order event attendee headquarter",
                "date_begin": fields.Date.today(),
                "date_end": fields.Date.today() + relativedelta(days=+7),
                "organizer_id": cls.customer.id,
                "customer_id": cls.customer.id,
                "resource_calendar_id": cls.resource_calendar.id,
                "main_responsible_id": user.id,
                "event_ticket_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.name,
                            "price": 55,
                        },
                    )
                ],
            }
        )
        track_vals = {
            "event_id": cls.event.id,
            "name": "Session 1",
            "date": fields.Date.today(),
            "partner_id": user.partner_id.id,
        }
        cls.env["event.track"].create(track_vals)
        sale_vals = {
            "headquarter_id": cls.customer.id,
            "partner_id": cls.customer.id,
            "partner_invoice_id": cls.customer.id,
            "partner_shipping_id": cls.customer.id,
            "company_id": cls.company.id,
        }
        cls.sale = cls.env["sale.order"].create(sale_vals)
        sale_line_vals = {
            "order_id": cls.sale.id,
            "product_id": cls.product.id,
            "name": cls.product.name,
            "product_uom_qty": 1,
            "product_uom": cls.product.uom_id.id,
            "price_unit": 100,
            "event_id": cls.event.id,
            "event_ticket_id": cls.event.event_ticket_ids[0].id,
        }
        cls.sale_order_line_obj.create(sale_line_vals)
        sale_line_vals = {
            "order_id": cls.sale.id,
            "product_id": cls.product.id,
            "name": cls.product_service.name,
            "product_uom_qty": 1,
            "product_uom": cls.product.uom_id.id,
            "price_unit": 100,
            "event_id": cls.event.id,
            "event_ticket_id": cls.event.event_ticket_ids[0].id,
        }
        cls.sale_order_line_obj.create(sale_line_vals)

    def test_sale_order_event_attendee_headquarter(self):
        self.sale.action_confirm()
        registration_vals = {
            "event_id": self.event.id,
            "sale_order_line_id": self.sale.order_line[1].id,
        }
        registration = self.registration_obj.create(registration_vals)
        registration.action_confirm()
        self.assertEqual(
            registration.sale_order_id.headquarter_id,
            registration.event_id.organizer_id,
        )
