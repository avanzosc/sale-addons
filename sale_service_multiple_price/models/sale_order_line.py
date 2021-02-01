# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    multiple_price_unit = fields.Float(
        string='Unit Price [Multiple Hour]',
        required=True,
        digits='Product Price',
        default=0.0)

    def _create_multiple_hour_invoice_line(self):
        analytic_line_obj = self.env["account.analytic.line"].sudo()
        for line in self.filtered(
                lambda l: l.qty_delivered_method == "timesheet" and
                l.multiple_price_unit):
            first_hour = multiple_hour = 0.0
            for timesheet in analytic_line_obj.search([
                    ("so_line", "=", line.id)]):
                first_hour += 1
                multiple_hour += timesheet.unit_amount - 1
            if multiple_hour:
                for invoice_line in line.invoice_lines:
                    new_invoice_line = invoice_line.copy_data(default={
                        "quantity": multiple_hour,
                        "price_unit": line.multiple_price_unit,
                        "sale_line_ids": [
                            (6, 0, invoice_line.sale_line_ids.ids)],
                    })
                    if new_invoice_line:
                        invoice_line.move_id.write({
                            "invoice_line_ids": [
                                (1, invoice_line.id, {"quantity": first_hour}),
                                (0, 0, new_invoice_line[0])],
                        })
