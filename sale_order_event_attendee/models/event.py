# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        for record in self:
            if record.order_status in ("draft", "sent"):
                order = record.sale_order_id
                record.write({"sale_order_line_id": None, "sale_order_id": None})
                order._calculate_order_line_qty()
            elif record.order_status in ("done", "sale"):
                raise ValidationError(
                    _(
                        "You cannot cancel a participant with a "
                        "confirmed Sale Order (Partner: {})."
                    ).format(record.partner_id.name)
                )

    def action_confirm(self):
        res = super(EventRegistration, self).action_confirm()
        for record in self:
            if not record.partner_id:
                continue
            select_ticket = record.event_ticket_id
            if not select_ticket:
                select_ticket = record.select_ticket()
            order = record.sale_order_id
            if select_ticket:
                line, order = record.get_event_attendee_sale_order(select_ticket)
                if not line:
                    if not order:
                        vals = record.event_attendee_catch_sale_order_vals()
                        order = self.env["sale.order"].sudo().create(vals)
                    line = record.event_attendee_create_sale_order_line(
                        order, select_ticket
                    )
                record.write({"sale_order_line_id": line.id, "sale_order_id": order.id})
            if order:
                order._calculate_order_line_qty()
        return res

    def get_event_attendee_sale_order(self, select_ticket):
        order_obj = self.env["sale.order"]
        line_obj = self.env["sale.order.line"]
        line = line_obj.search(
            [
                ("order_partner_id", "=", self.partner_id.id),
                ("state", "in", ("draft", "sent")),
                ("event_id", "=", self.event_id.id),
                ("event_ticket_id", "=", select_ticket.id),
            ],
            limit=1,
        )
        order = line.order_id if line else order_obj
        if not order:
            order = order_obj.search(
                [
                    ("partner_id", "=", self.partner_id.id),
                    ("state", "in", ("draft", "sent")),
                ],
                order="date_order desc",
                limit=1,
            )
        return line, order

    def event_attendee_catch_sale_order_vals(self):
        return {"partner_id": self.partner_id.id}

    def event_attendee_create_sale_order_line(self, order, select_ticket):
        ticket_line = order.order_line.filtered(
            lambda ln: ln.product_id.id == select_ticket.product_id.id
            and ln.event_id.id == self.event_id.id
        )
        order_line = None
        if not ticket_line:
            vals = self.event_attendee_catch_values_for_sale_order_line(order)
            order_line = self.env["sale.order.line"].sudo().create(vals)
        else:
            for line in ticket_line:
                if line.product_id.id == select_ticket.product_id.id:
                    order_line = line
                    break
        return order_line

    def event_attendee_catch_values_for_sale_order_line(self, order):
        vals = {
            "product_id": self.event_ticket_id.product_id.id,
            "event_id": self.event_id.id,
            "event_ticket_id": self.event_ticket_id.id,
            "name": self.event_ticket_id.name,
            "order_id": order.id,
            "product_uom": self.event_ticket_id.product_id.uom_id.id,
        }
        return vals

    def select_ticket(self):
        self.ensure_one()
        select_ticket = None
        if not self.event_id:
            raise ValidationError(_("There is no event selected!"))
        available_tickets = self.event_id.event_ticket_ids
        if len(available_tickets) == 1:
            select_ticket = available_tickets
        elif len(available_tickets) > 1:
            member_ticket = available_tickets.filtered(lambda t: t.is_member)
            if self.is_member:
                select_ticket = member_ticket
            elif member_ticket and len(available_tickets) == 2:
                select_ticket = available_tickets.filtered(lambda t: not t.is_member)
            else:
                raise ValidationError(_("You must select a ticket by hand."))
        if select_ticket:
            self.write({"event_ticket_id": select_ticket.id})
        return select_ticket
