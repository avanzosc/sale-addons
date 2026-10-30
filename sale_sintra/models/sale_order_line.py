# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    ib_code = fields.Char(string="IB Code")
    sintra_id = fields.Many2one(string="Sintra", related="order_id.sintra_id")
    sintra_state = fields.Selection(
        string="Sintra Status", related="order_id.sintra_state"
    )
    sintra_partner_id = fields.Many2one(
        string="Sintra Customer", related="order_id.sintra_partner_id"
    )
    sintra_project = fields.Char(
        string="Sintra Project", related="order_id.sintra_project"
    )
    sintra_registration = fields.Char(
        string="Sintra Registration", related="order_id.sintra_registration"
    )
    sintra_work = fields.Char(string="Sintra Work", related="order_id.sintra_work")
    sintra_installation_code = fields.Char(
        string="Sintra Installation Code",
        related="order_id.sintra_installation_code",
    )
    sintra_installation = fields.Text(
        string="Sintra Installation", related="order_id.sintra_installation"
    )
    sintra_features = fields.Char(
        string="Sintra Features", related="order_id.sintra_features"
    )
    sintra_purchase_id = fields.Many2one(
        string="Sintra Cabinet Purchase Order",
        related="order_id.sintra_purchase_id",
    )
    sintra_delivery_date = fields.Datetime(
        string="Sintra Delivery Date", related="order_id.sintra_delivery_date"
    )
    sintra_planned_date = fields.Datetime(
        string="Sintra Planned Date", related="order_id.sintra_planned_date"
    )
    sintra_note = fields.Text(string="Sintra Note", related="order_id.sintra_note")
    sintra_region = fields.Selection(
        string="Sintra Region", related="order_id.sintra_region"
    )
    sintra_zone = fields.Char(string="Sintra Zone", related="order_id.sintra_zone")
    sintra_utd = fields.Char(string="Sintra UTD", related="order_id.sintra_utd")
    sintra_sales_notified = fields.Boolean(
        string="Sintra Email Sent to Sales",
        related="order_id.sintra_sales_notified",
    )
    sintra_ib_delivery_date = fields.Datetime(
        string="Sintra IB Delivery Date", related="order_id.sintra_ib_delivery_date"
    )
    sintra_installer = fields.Text(
        string="Sintra Installer", related="order_id.sintra_installer"
    )
    sintra_ib_manager = fields.Char(
        string="Sintra IB Manager", related="order_id.sintra_ib_manager"
    )
    sintra_sim = fields.Char(string="Sintra SIM", related="order_id.sintra_sim")
