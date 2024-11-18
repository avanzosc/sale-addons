from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

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
    training = fields.Text(
        string="Training",
    )
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
        string="Delivery Timetable",
        default=lambda self: self.partner_id.delivery_timetable,
        store=True,
    )
