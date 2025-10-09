from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class SaleReport(models.Model):
    _inherit = "sale.report"

    qty_pending_delivery = fields.Float(
        string="Pending Delivery Qty",
        readonly=True,
    )
    qty_pending_invoicing = fields.Float(
        string="Pending Invoicing Qty",
        readonly=True,
    )
    amount_pending_delivery = fields.Float(
        string="Pending Delivery Amount",
        readonly=True,
    )
    amount_pending_invoicing = fields.Float(
        string="Pending Invoicing Amount",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res.update({
    "qty_pending_delivery": "COALESCE(SUM(l.qty_pending_delivery), 0)",
    "qty_pending_invoicing": "COALESCE(SUM(l.qty_pending_invoicing), 0)",
    "amount_pending_delivery": (
        "COALESCE(SUM(l.amount_pending_delivery), 0)"
    ),
    "amount_pending_invoicing": (
        "COALESCE(SUM(l.amount_pending_invoicing), 0)"
    ),
})
        return res
        
