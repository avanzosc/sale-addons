# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sintra_id = fields.Many2one(
        comodel_name="sale.sintra", string="Sintra", copy=False, index=True
    )
    sintra_state = fields.Selection(
        string="Sintra Status", related="sintra_id.state", readonly=False
    )
    sintra_partner_id = fields.Many2one(
        string="Sintra Customer", related="sintra_id.partner_id", readonly=False
    )
    sintra_project = fields.Char(
        string="Sintra Project", related="sintra_id.project", readonly=False
    )
    sintra_registration = fields.Char(
        string="Sintra Registration", related="sintra_id.registration", readonly=False
    )
    sintra_work = fields.Char(
        string="Sintra Work", related="sintra_id.work", readonly=False
    )
    sintra_installation_code = fields.Char(
        string="Sintra Installation Code",
        related="sintra_id.installation_code",
        readonly=False,
    )
    sintra_installation = fields.Text(
        string="Sintra Installation", related="sintra_id.installation", readonly=False
    )
    sintra_features = fields.Char(
        string="Sintra Features", related="sintra_id.features", readonly=False
    )
    sintra_purchase_id = fields.Many2one(
        string="Sintra Cabinet Purchase Order",
        related="sintra_id.purchase_id",
        readonly=False,
    )
    sintra_delivery_date = fields.Datetime(
        string="Sintra Delivery Date", related="sintra_id.delivery_date", readonly=False
    )
    sintra_planned_date = fields.Datetime(
        string="Sintra Planned Date", related="sintra_id.planned_date", readonly=False
    )
    sintra_note = fields.Text(
        string="Sintra Note", related="sintra_id.note", readonly=False
    )
    sintra_region = fields.Selection(
        string="Sintra Region", related="sintra_id.region", readonly=False
    )
    sintra_zone = fields.Char(
        string="Sintra Zone", related="sintra_id.zone", readonly=False
    )
    sintra_utd = fields.Char(
        string="Sintra UTD", related="sintra_id.utd", readonly=False
    )
    sintra_sales_notified = fields.Boolean(
        string="Sintra Email Sent to Sales",
        related="sintra_id.sales_notified",
        readonly=False,
    )
    sintra_ib_delivery_date = fields.Datetime(
        string="Sintra IB Delivery Date",
        related="sintra_id.ib_delivery_date",
        readonly=False,
    )
    sintra_installer = fields.Text(
        string="Sintra Installer", related="sintra_id.installer", readonly=False
    )
    sintra_ib_manager = fields.Char(
        string="Sintra IB Manager", related="sintra_id.ib_manager", readonly=False
    )
    sintra_sim = fields.Char(
        string="Sintra SIM", related="sintra_id.sim", readonly=False
    )
    sintra_document_ids = fields.One2many(
        string="Sintra Documents", related="sintra_id.document_ids", readonly=False
    )
    sintra_editable = fields.Boolean(compute="_compute_sintra_editable")

    @api.depends_context("uid")
    def _compute_sintra_editable(self):
        editable = self.env.user.has_group("sale_sintra.group_sintra_manager")
        for order in self:
            order.sintra_editable = editable
