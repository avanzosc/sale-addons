from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_delivery_timetable(self):
        partner_id = self.env.context.get("default_partner_id")
        if not partner_id:
            return False
        return self.env["res.partner"].browse(partner_id).delivery_timetable

    @api.onchange("partner_id")
    def _onchange_partner_delivery_timetable(self):
        for order in self:
            order.delivery_timetable = order.partner_id.delivery_timetable

    integrator_id = fields.Many2one(
        "res.partner",
        string="Integrator",
    )
    sale_phone = fields.Char(
        string="Contact Phone for Delivery",
    )
    delivery_note = fields.Text(
        string="Delivery Notes",
    )
    install_address_id = fields.Many2one(
        "res.partner",
        string="Installation Address",
    )
    install_date = fields.Date(
        string="Estimated Installation Date",
    )
    install_type_id = fields.Many2one(
        "install.type",
        string="Installation Type",
    )
    technical_contact_id = fields.Many2one(
        "res.partner",
        string="Technical Contact",
    )
    training = fields.Text()
    installation_done_by_id = fields.Many2one(
        "res.partner",
        string="Installation Done By",
    )
    structure_type_id = fields.Many2one(
        "structure.type",
        string="Structure Type",
    )
    initial_order_id = fields.Many2one(
        "sale.order",
        string="Initial Order",
        domain="[('partner_id', '=', partner_id)]",
    )
    delivery_timetable = fields.Char(
        default=_default_delivery_timetable,
        store=True,
    )
