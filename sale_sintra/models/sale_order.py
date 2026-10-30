# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sintra_id = fields.Many2one(
        comodel_name="sale.sintra", string="Sintra", copy=False, index=True
    )
    sintra_state = fields.Selection(string="Sintra Status", related="sintra_id.state")
    sintra_partner_id = fields.Many2one(
        string="Sintra Customer", related="sintra_id.partner_id"
    )
    sintra_project = fields.Char(string="Sintra Project", related="sintra_id.project")
    sintra_registration = fields.Char(
        string="Sintra Registration", related="sintra_id.registration"
    )
    sintra_work = fields.Char(string="Sintra Work", related="sintra_id.work")
    sintra_installation_code = fields.Char(
        string="Sintra Installation Code", related="sintra_id.installation_code"
    )
    sintra_installation = fields.Text(
        string="Sintra Installation", related="sintra_id.installation"
    )
    sintra_features = fields.Char(
        string="Sintra Features", related="sintra_id.features"
    )
    sintra_purchase_id = fields.Many2one(
        string="Sintra Cabinet Purchase Order", related="sintra_id.purchase_id"
    )
    sintra_delivery_date = fields.Datetime(
        string="Sintra Delivery Date", related="sintra_id.delivery_date"
    )
    sintra_planned_date = fields.Datetime(
        string="Sintra Planned Date", related="sintra_id.planned_date"
    )
    sintra_note = fields.Text(string="Sintra Note", related="sintra_id.note")
    sintra_region = fields.Selection(string="Sintra Region", related="sintra_id.region")
    sintra_zone = fields.Char(string="Sintra Zone", related="sintra_id.zone")
    sintra_utd = fields.Char(string="Sintra UTD", related="sintra_id.utd")
    sintra_sales_notified = fields.Boolean(
        string="Sintra Email Sent to Sales", related="sintra_id.sales_notified"
    )
    sintra_ib_delivery_date = fields.Datetime(
        string="Sintra IB Delivery Date", related="sintra_id.ib_delivery_date"
    )
    sintra_installer = fields.Text(
        string="Sintra Installer", related="sintra_id.installer"
    )
    sintra_ib_manager = fields.Char(
        string="Sintra IB Manager", related="sintra_id.ib_manager"
    )
    sintra_sim = fields.Char(string="Sintra SIM", related="sintra_id.sim")
    sintra_document_ids = fields.One2many(
        string="Sintra Documents", related="sintra_id.document_ids"
    )
