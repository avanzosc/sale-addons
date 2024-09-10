from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_timetable = fields.Char(
        string="Delivery Timetable",
        related="sale_id.delivery_timetable",
        store=True,
    )
    sale_phone = fields.Char(
        string="Contact Phone for Delivery",
        related="sale_id.sale_phone",
        store=True,
    )
    delivery_note = fields.Text(
        string="Delivery Notes",
        related="sale_id.delivery_note",
        store=True,
    )
    install_address_id = fields.Many2one(
        "res.partner",
        string="Installation Address",
        related="sale_id.install_address_id",
        store=True,
    )
    install_date = fields.Date(
        string="Estimated Installation Date",
        related="sale_id.install_date",
        store=True,
    )
    install_type_id = fields.Many2one(
        "install.type",
        string="Installation Type",
        related="sale_id.install_type_id",
        store=True,
    )
    technical_contact_id = fields.Many2one(
        "res.partner",
        string="Technical Contact",
        related="sale_id.technical_contact_id",
        store=True,
    )
    training = fields.Text(
        string="Training",
        related="sale_id.training",
        store=True,
    )
    installation_done_by_id = fields.Many2one(
        "res.partner",
        string="Installation Done By",
        related="sale_id.installation_done_by_id",
        store=True,
    )
    structure_type_id = fields.Many2one(
        "structure.type",
        string="Structure Type",
        related="sale_id.structure_type_id",
        store=True,
    )
    initial_order_id = fields.Many2one(
        "sale.order",
        string="Initial Order",
        related="sale_id.initial_order_id",
        store=True,
    )
