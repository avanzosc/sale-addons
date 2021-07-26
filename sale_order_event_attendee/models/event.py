
from odoo import models, _
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_cancel(self):
        super(EventRegistration, self).action_cancel()
        if self.order_status in ('draft', 'sent'):
            order = self.sale_order_id
            self.write({
                'sale_order_line_id': None,
                'sale_order_id': None})
            order._calculate_order_line_qty()
        elif self.order_status in ('done', 'sale'):
            raise ValidationError(
                _("You cannot cancel a participant with a "
                  "confirmed Sale Order."))

    def action_confirm(self):
        res = super(EventRegistration, self).action_confirm()
        if not self.partner_id:
            return

        select_ticket = self.event_ticket_id
        if not select_ticket:
            select_ticket = self.select_ticket()

        order = self.sale_order_id
        if select_ticket:
            if not order:
                order_obj = self.env['sale.order']
                order = order_obj.search([
                    ('partner_id', '=', self.partner_id.id),
                    ('state', 'in', ('draft', 'sent'))
                ], order='date_order desc', limit=1)
                if not order:
                    order = order_obj.sudo().create({
                        'partner_id': self.partner_id.id
                    })
                self.write({'sale_order_id': order.id})

            if not self.sale_order_line_id:
                ticket_line = order.order_line.filtered(
                    lambda l:
                    l.product_id.id == select_ticket.product_id.id)
                order_line = None
                if not ticket_line:
                    order_line = self.env['sale.order.line'].sudo().create(
                        {
                            'product_id': self.event_ticket_id.product_id.id,
                            'event_id': self.event_id.id,
                            'name': self.event_ticket_id.name,
                            'order_id': order.id,
                            'product_uom':
                                self.event_ticket_id.product_id.uom_id.id})
                else:
                    for line in ticket_line:
                        if line.product_id.id == select_ticket.product_id.id:
                            order_line = line
                            break
                self.write({'sale_order_line_id': order_line.id})

        if order:
            order._calculate_order_line_qty()

        return res

    def select_ticket(self):
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
