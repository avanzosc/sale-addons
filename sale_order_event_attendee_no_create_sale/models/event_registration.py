# Copyright 2023 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_cancel(self):
        return super(EventRegistration, self.with_context(
            no_remove_sale_order_info=True)).action_cancel()

    def get_event_attendee_sale_order(self, select_ticket):
        if self.sale_order_id and self.sale_order_line_id:
            return self.sale_order_line_id, self.sale_order_id
        return super(EventRegistration, self).get_event_attendee_sale_order(
            select_ticket)

    def write(self, vals):
        if ("no_remove_sale_order_info" in self.env.context and
                self.env.context.get("no_remove_sale_order_info", False)):
            if "sale_order_id" in vals:
                del vals["sale_order_id"]
            if "sale_order_line_id" in vals:
                del vals["sale_order_line_id"]
        result = super(EventRegistration, self).write(vals)
        return result
