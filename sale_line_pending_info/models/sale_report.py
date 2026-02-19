from odoo import fields, models


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
        currency_rate = self._case_value_or_one("s.currency_rate")
        company_rate = self._case_value_or_one("account_currency_table.rate")
        pending_delivery_amount_sql = (
            "CASE WHEN l.product_id IS NOT NULL THEN "
            f"SUM(l.amount_pending_delivery / {currency_rate}"
            f" * {company_rate}) ELSE 0 END"
        )
        pending_invoicing_amount_sql = (
            "CASE WHEN l.product_id IS NOT NULL THEN "
            f"SUM(l.amount_pending_invoicing / {currency_rate}"
            f" * {company_rate}) ELSE 0 END"
        )
        res.update(
            {
                "qty_pending_delivery": (
                    "CASE WHEN l.product_id IS NOT NULL THEN "
                    "SUM(l.qty_pending_delivery / u.factor * u2.factor) "
                    "ELSE 0 END"
                ),
                "qty_pending_invoicing": (
                    "CASE WHEN l.product_id IS NOT NULL THEN "
                    "SUM(l.qty_pending_invoicing / u.factor * u2.factor) "
                    "ELSE 0 END"
                ),
                "amount_pending_delivery": pending_delivery_amount_sql,
                "amount_pending_invoicing": pending_invoicing_amount_sql,
            }
        )
        return res
