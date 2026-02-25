# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _normalize_report_url(self, raw_url):
        if not raw_url:
            return False
        if not isinstance(raw_url, str):
            raw_url = str(raw_url)
        url = raw_url.strip()
        if not url:
            return False

        if url.lower() in {"0", "0.0", "false", "none", "null"}:
            return False

        if url.startswith(("http://", "https://")):
            return url

        if "://" not in url and "." in url and " " not in url:
            return f"https://{url}"

        return False

    def _get_product_origin_for_report(self):
        self.ensure_one()
        product = self.product_id
        if not product:
            return False
        origin = product.description_sale or product.product_tmpl_id.description_sale
        if not origin:
            return False
        origin = origin.strip()
        line_title = (self.name or "").split("\n")[0].strip()
        if line_title and origin.lower() == line_title.lower():
            return False
        return origin

    def _get_product_external_url_for_report(self):
        self.ensure_one()
        product = self.product_id
        if not product:
            return False

        if "external_url" in product._fields and product.external_url:
            url = self._normalize_report_url(product.external_url)
            if url:
                return url
        if (
            "external_url" in product.product_tmpl_id._fields
            and product.product_tmpl_id.external_url
        ):
            url = self._normalize_report_url(product.product_tmpl_id.external_url)
            if url:
                return url

        if "website_link" in product._fields and product.website_link:
            url = self._normalize_report_url(product.website_link)
            if url:
                return url
        if (
            "website_link" in product.product_tmpl_id._fields
            and product.product_tmpl_id.website_link
        ):
            url = self._normalize_report_url(product.product_tmpl_id.website_link)
            if url:
                return url

        return False
