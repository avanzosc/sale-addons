# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    recurring_interval = fields.Integer(string="Invoice Every", default=0)
    recurring_rule_type = fields.Selection(
        [
            ("daily", _("Day(s)")),
            ("weekly", _("Week(s)")),
            ("monthly", _("Month(s)")),
            ("monthlylastday", _("Month(s) last day")),
            ("quarterly", _("Quarter(s)")),
            ("semesterly", _("Semester(s)")),
            ("yearly", _("Year(s)")),
        ],
        string="Recurrence",
    )
    apply_recurrence_in = fields.Selection(
        [("contract", _("Contract")), ("line", _("Contract line"))],
        string="Apply recurrence in",
    )

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        return product

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if "no_update_product" not in self.env.context and (
            "recurring_interval" in vals
            or "recurring_rule_type" in vals
            or "apply_recurrence_in" in vals
        ):
            for template in self:
                if template.product_variant_count == 1:
                    variant = template.product_variant_ids[0]
                    variant_vals = {
                        "recurring_interval": template.recurring_interval,
                        "recurring_rule_type": template.recurring_rule_type,
                        "apply_recurrence_in": template.apply_recurrence_in,
                    }
                    variant.with_context(no_update_template=True).write(variant_vals)
        return result
