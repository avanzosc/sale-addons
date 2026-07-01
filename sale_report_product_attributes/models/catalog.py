
from odoo import _, models


class ProductCatalogWeb(models.Model):
    _inherit = 'product.catalog.web'

    def button_open_product_catalog_product_attrs(self):
        self.ensure_one()
        action = self.env.ref(
            "sale_report_product_attributes."
            "action_product_attribute_catalog_report")
        action_dict = action.read()[0] if action else {}
        # domain = expression.AND([
        #     [("catalog_id", "=", self.id)],
        #     safe_eval(action.domain or "[]")
        # ])
        action_dict.update({
            "display_name": _("Catalogue Product Attributes"),
            "context": "{'search_default_catalog_id': [active_id]}"

           # "domain": domain,
        })
        return action_dict

    def action_wizard_catalog_attributes_report(self):
        self.ensure_one()
        return {
            "name": _("Equipment Request"),
            "type": "ir.actions.act_window",
            "res_model": "catalog.attribute.partner.report",
            "view_mode": "form",
           # "domain": [("id", "in", self.equipment_request_ids.ids)]
        }
