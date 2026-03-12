# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    lot_name = fields.Char(
        string="Lot Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    lot_id = fields.Many2one(
        string="Lot",
        comodel_name="stock.production.lot",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        line_values = super().action_validate()
        for item in line_values:
            # item is (1, line_id, update_values)
            line = self.browse(item[1])
            if line.lot_name and not item[2].get("log_info"):
                data = {"log_info": item[2].get("log_info") or ""}
                data = line._check_lot(data)
                if data.get("log_info"):
                    item[2]["log_info"] = data["log_info"]
                    item[2]["state"] = "error"
                    item[2]["action"] = "nothing"
                else:
                    item[2]["lot_id"] = (
                        data["sale_lot"].id if data.get("sale_lot") else False
                    )
        return line_values

    def _check_lot(self, data):
        log_info = data.get("log_info", "")
        lot = False
        if self.lot_name:
            domain = [("name", "=", self.lot_name)]
            if self.sale_product_id:
                domain.append(("product_id", "=", self.sale_product_id.id))
            lots = self.env["stock.production.lot"].search(domain)
            if not lots:
                error = _("Error: No lot found with name '%s'.") % self.lot_name
                log_info = error if not log_info else "{} {}".format(log_info, error)
            elif len(lots) > 1:
                error = (
                    _("Error: More than one lot found with name '%s'.") % self.lot_name
                )
                log_info = error if not log_info else "{} {}".format(log_info, error)
            else:
                lot = lots
        data["sale_lot"] = lot
        data["log_info"] = log_info
        return data

    def _get_update_values(self, data, state, action):
        update_values = super()._get_update_values(data, state, action)
        if data.get("sale_lot"):
            update_values["lot_id"] = data["sale_lot"].id
        return update_values

    def _sale_order_line_values(self):
        values = super()._sale_order_line_values()
        if self.lot_id:
            values["lot_id"] = self.lot_id.id
        return values

    def _create_sale_order_line(self, sale):
        super()._create_sale_order_line(sale)
        if self.lot_id:
            last_line = sale.order_line[-1]
            last_line.lot_id = self.lot_id
