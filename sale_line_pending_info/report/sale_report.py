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

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res.update(
            {
                "qty_pending_delivery": """
            CASE WHEN l.product_id IS NOT NULL THEN
            SUM(l.qty_pending_delivery / u.factor * u2.factor) ELSE 0
            END
            """,
                "qty_pending_invoicing": """
            CASE WHEN l.product_id IS NOT NULL THEN
            SUM(l.qty_pending_invoicing / u.factor * u2.factor) ELSE 0
            END
        """,
                "amount_pending_delivery": f"""
            CASE WHEN l.product_id IS NOT NULL THEN SUM(l.amount_pending_delivery
            / {self._case_value_or_one('s.currency_rate')}
            * {self._case_value_or_one('currency_table.rate')}) ELSE 0
            END
        """,
                "amount_pending_invoicing": f"""
            CASE WHEN l.product_id IS NOT NULL THEN SUM(l.amount_pending_invoicing
            / {self._case_value_or_one('s.currency_rate')}
            * {self._case_value_or_one('currency_table.rate')}) ELSE 0
            END
        """,
            }
        )
        return res
