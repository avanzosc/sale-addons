# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _compute_attachment_ids(self):
        res = super()._compute_attachment_ids()

        for composer in self:
            model = (
                composer.model
                or composer.env.context.get("active_model")
                or composer.env.context.get("default_model")
            )
            if model != "sale.order":
                continue

            res_ids = composer._evaluate_res_ids()
            if len(res_ids) != 1:
                continue

            sale = composer.env["sale.order"].browse(res_ids[0])
            line_ids = sale.order_line.ids
            if not line_ids:
                continue

            attaches = (
                composer.env["ir.attachment"]
                .sudo()
                .search(
                    [
                        ("res_model", "=", "sale.order.line"),
                        ("res_id", "in", line_ids),
                    ]
                )
            )
            if not attaches:
                continue

            existing_names = set(composer.attachment_ids.mapped("name"))
            to_add = composer.env["ir.attachment"]
            for att in attaches:
                if att.name in existing_names:
                    continue
                copied = att.with_user(composer.env.user).copy(
                    {
                        "res_model": composer._name,
                        "res_id": composer.id,
                    }
                )
                to_add |= copied
                existing_names.add(att.name)

            if to_add:
                composer.attachment_ids |= to_add

        return res
