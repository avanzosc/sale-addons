
from odoo import models, _
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        for record in self:
            if record.order_status in ('draft', 'sent'):
                order = record.sale_order_id
                record.write({
                    'sale_order_line_id': None,
                    'sale_order_id': None})
                order._calculate_order_line_qty()
            elif record.order_status in ('done', 'sale'):
                raise ValidationError(
                    _("You cannot cancel a participant with a "
                      "confirmed Sale Order (Partner: {}).").format(
                        record.partner_id.name))

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
                line, order = record.get_event_attendee_order(
                    select_ticket)
                if not order:
                    order = self.env['sale.order'].sudo().create({
                        'partner_id': self.partner_id.id
                    })
                if not line:
                    line = record.get_event_attendee_order_line(
                        order, select_ticket)
                record.write({
                    'sale_order_line_id': line.id,
                    'sale_order_id': order.id
                })
            if order:
                order._calculate_order_line_qty()

        return res

    def get_event_attendee_order(self, select_ticket):
        # Find open order line for parner and ticket
        line_obj = self.env['sale.order.line']
        line = line_obj.search([
            ('order_partner_id', '=', self.partner_id.id),
            ('state', 'in', ('draft', 'sent')),
            ('event_id', '=', self.event_id.id),
            ('event_ticket_id', '=', select_ticket.id),
        ], limit=1)
        order = line.order_id

        if not order:
            # Find open order for partner
            order_obj = self.env['sale.order']
            order = order_obj.search([
                ('partner_id', '=', self.partner_id.id),
                ('state', 'in', ('draft', 'sent'))
            ], order='date_order desc', limit=1)

        return line, order

    def get_event_attendee_order_line(self, order, select_ticket):
        ticket_line = order.order_line.filtered(
            lambda l:
            l.product_id.id == select_ticket.product_id.id)
        order_line = None
        if not ticket_line:
            order_line = self.env['sale.order.line'].sudo().create(
                {
                    'product_id': self.event_ticket_id.product_id.id,
                    'event_id': self.event_id.id,
                    'event_ticket_id': self.event_ticket_id.id,
                    'name': self.event_ticket_id.name,
                    'order_id': order.id,
                    'product_uom':
                        self.event_ticket_id.product_id.uom_id.id})
        else:
            for line in ticket_line:
                if line.product_id.id == select_ticket.product_id.id:
                    order_line = line
                    break
        return order_line

    def select_ticket(self):
        self.ensure_one()
        select_ticket = None
        if not self.event_id:
            raise ValidationError(
                _("There is no event selected!"))
        available_tickets = self.event_id.event_ticket_ids
        if len(available_tickets) == 1:
            select_ticket = available_tickets
        elif len(available_tickets) > 1:
            member_ticket = available_tickets.filtered(lambda t: t.is_member)
            if self.is_member:
                select_ticket = member_ticket
            elif member_ticket and len(available_tickets) == 2:
                select_ticket = available_tickets.filtered(
                    lambda t: not t.is_member)
            else:
                raise ValidationError(
                    _("You must select a ticket by hand."))
        if select_ticket:
            self.write({'event_ticket_id': select_ticket.id})

        return select_ticket
