from odoo import models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def write(self, values):
        result = super(EventRegistration, self).write(values)
        if "sale_order_id" in values and values.get("sale_order_id", False):
            sale_order = self.env["sale.order"].browse(values.get("sale_order_id"))
            for registration in self.filtered(
                lambda x: x.event_id and x.event_id.organizer_id
            ):
                sale_order.headquarter_id = registration.event_id.organizer_id.id
        return result
