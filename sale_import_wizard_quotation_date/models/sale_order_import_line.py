# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from datetime import datetime
import pytz


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    def _sale_order_values(self):
        values = super(SaleOrderImportLine, self)._sale_order_values()
        if self.date_order:
            date_order = "{} 08:00:00".format(
                fields.Date.to_string(self.date_order))
            date_order = datetime.strptime(
                date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get('tz') or 'UTC')
            date_order = timezone.localize(
                date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            values["quotation_date"] = date_order
        return values
