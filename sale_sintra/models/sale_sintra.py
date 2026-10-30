# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleSintra(models.Model):
    _name = "sale.sintra"
    _description = "Sintra"
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(string="Objective", required=True, copy=False)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("pending", "Pending Sales"),
            ("unplanned", "Unplanned"),
            ("planned", "Planned"),
            ("tested", "Tested"),
            ("sent", "Sent"),
            ("received", "Received"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        copy=False,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer")
    project = fields.Char()
    registration = fields.Char()
    work = fields.Char()
    installation_code = fields.Char()
    installation = fields.Text()
    features = fields.Char()
    purchase_id = fields.Many2one(
        comodel_name="purchase.order", string="Cabinet Purchase Order", copy=False
    )
    delivery_date = fields.Datetime()
    planned_date = fields.Datetime()
    note = fields.Text()
    region = fields.Selection(
        selection=[
            ("1-N", "1-North"),
            ("2-O", "2-West"),
            ("4-E", "4-East"),
            ("5-C", "5-Center"),
        ],
        default="1-N",
    )
    zone = fields.Char()
    utd = fields.Char(string="UTD")
    sales_notified = fields.Boolean(string="Email Sent to Sales", copy=False)
    ib_delivery_date = fields.Datetime(string="IB Delivery Date")
    installer = fields.Text()
    ib_manager = fields.Char(string="IB Manager")
    sim = fields.Char(string="SIM")
    document_ids = fields.One2many(
        comodel_name="sale.sintra.document",
        inverse_name="sintra_id",
        string="Documents",
        copy=True,
    )
    sale_order_ids = fields.One2many(
        comodel_name="sale.order", inverse_name="sintra_id", string="Sales Orders"
    )

    _sql_constraints = [
        (
            "name_unique",
            "UNIQUE (name)",
            "The objective must be unique.",
        ),
    ]

    def action_send_sales_notice(self):
        partners = self.env.ref("sale_sintra.group_sintra_sales_notice").users.mapped(
            "partner_id"
        )
        if not partners:
            raise UserError(
                _(
                    "No user receives the Sintra notice to Sales. Add them to the "
                    "group 'Receive Sintra Notice to Sales'."
                )
            )
        for sintra in self:
            sintra.message_post_with_source(
                "sale_sintra.mail_template_sales_notice",
                partner_ids=partners.ids,
                subtype_xmlid="mail.mt_comment",
            )
        self.write({"sales_notified": True, "state": "pending"})
