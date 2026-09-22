# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.tools import get_lang


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("product_id", "move_id.ref", "move_id.payment_reference")
    def _compute_name(self):
        result = super()._compute_name()
        for line in self.filtered(
            lambda z: z.journal_id.type == "sale"
            and z.display_type == "product"
            and z.product_id
            and z.product_id.no_product_description_to_sale_invoice_lines
        ):
            product_lang = line.product_id.with_context(
                lang=get_lang(self.env, line.move_id.partner_id.lang).code,
                partner_id=None,
                company_id=line.company_id.id,
            )
            product_lang_name = product_lang.display_name
            if product_lang_name in line.name:
                line.name = line.name.replace(product_lang_name, "").strip()
        return result
