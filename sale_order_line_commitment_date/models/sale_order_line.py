# © 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(
        string="Delivery Date",
        related="order_id.commitment_date",
        store=True)
    type_id = fields.Many2one(
        string="Sale Type",
        comodel_name="sale.order.type",
        related="order_id.type_id",
        store=True)
    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="type_id.warehouse_id",
        store=True)
