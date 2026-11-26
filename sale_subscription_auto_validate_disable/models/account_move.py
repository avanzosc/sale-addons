from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    subscription_auto_validate_draft = fields.Boolean(
        string="Subscription automatic draft",
        copy=False,
    )

    def _post(self, soft=True):
        posted_moves = super()._post(soft=soft)
        subscription_invoices = posted_moves.filtered(
            lambda move: move.subscription_auto_validate_draft
            and move.move_type == "out_invoice"
            and move.state == "posted"
        )

        for invoice in subscription_invoices:
            subscriptions = invoice.invoice_line_ids.subscription_id
            subscriptions.with_context(mail_notrack=True).write(
                {
                    "payment_exception": False,
                }
            )
        return posted_moves
