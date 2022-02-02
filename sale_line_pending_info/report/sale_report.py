# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    qty_pending_delivery = fields.Float(
        string="Pending delivery qty",
        readonly=True,
    )
    qty_pending_invoicing = fields.Float(
        string="Pending invoicing qty",
        readonly=True,
    )
    amount_pending_delivery = fields.Float(
        string="Amount pending delivery",
        readonly=True,
    )
    amount_pending_invoicing = fields.Float(
        string="Amount pending invoicing",
        readonly=True,
    )

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if not fields:
            fields = {}
        fields["qty_pending_delivery"] = (
            ", sum(l.qty_pending_delivery / u.factor * u2.factor) as "
            "qty_pending_delivery"
        )
        fields["qty_pending_invoicing"] = (
            ", sum(l.qty_pending_invoicing / u.factor * u2.factor) as "
            "qty_pending_invoicing"
        )
        fields["amount_pending_delivery"] = (
            ", sum(l.amount_pending_delivery / CASE COALESCE(s.currency_rate,"
            " 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as "
            "amount_pending_delivery"
        )
        fields["amount_pending_invoicing"] = (
            ", sum(l.amount_pending_invoicing / CASE COALESCE(s.currency_rate,"
            " 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as "
            "amount_pending_invoicing"
        )
        return super(SaleReport, self)._query(
            with_clause=with_clause,
            fields=fields,
            groupby=groupby,
            from_clause=from_clause,
        )
