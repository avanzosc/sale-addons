# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New") and vals.get("partner_id"):
                partner = self.env["res.partner"].browse(vals["partner_id"])
                if not partner.ref:
                    raise ValidationError(
                        _("Customer '%s' without reference.") % partner.display_name
                    )
                seq_date = (
                    fields.Datetime.context_timestamp(
                        self, fields.Datetime.to_datetime(vals["date_order"])
                    )
                    if vals.get("date_order")
                    else None
                )
                seq = (
                    self.env["ir.sequence"]
                    .with_company(vals.get("company_id"))
                    .next_by_code("sale.order.sequence", sequence_date=seq_date)
                    or "00001"
                )
                seq = str(seq).zfill(5)
                vals["name"] = f"AR-{partner.ref}-{seq}"
        return super().create(vals_list)
