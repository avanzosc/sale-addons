# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    manual_sequence = fields.Char(string="Manual seq.")

    @api.model
    def _move_autocomplete_invoice_lines_create(self, vals_list):
        new_vals_list = super()._move_autocomplete_invoice_lines_create(vals_list)
        for old in vals_list:
            data = False
            if "invoice_line_ids" in old:
                for line in old.get("invoice_line_ids"):
                    if (
                        len(line) == 3
                        and line[0] == 0
                        and not str(line[1]).isdigit()
                        and "virtual" in line[1]
                        and "manual_sequence" in line[2]
                    ):
                        data = line
                        for new in new_vals_list:
                            if "line_ids" in new:
                                for line in new.get("line_ids"):
                                    if (
                                        len(line) == 3
                                        and line[0] == 0
                                        and not str(data[1]).isdigit()
                                        and "virtual" in line[1]
                                        and line[1] == data[1]
                                    ):
                                        line[2]["manual_sequence"] = data[2].get(
                                            "manual_sequence", ""
                                        )
        return new_vals_list

    def _move_autocomplete_invoice_lines_write(self, vals):
        if "invoice_line_ids" in vals:
            for line in vals.get("invoice_line_ids"):
                if (
                    len(line) == 3
                    and line[0] == 0
                    and not str(line[1]).isdigit()
                    and "virtual" in line[1]
                    and "manual_sequence" in line[2]
                ):
                    data = line
                    if "line_ids" in vals:
                        for line in vals.get("line_ids"):
                            if (
                                len(line) == 3
                                and line[0] == 0
                                and not str(data[1]).isdigit()
                                and "virtual" in line[1]
                                and line[1] == data[1]
                            ):
                                line[2]["manual_sequence"] = data[2].get(
                                    "manual_sequence", ""
                                )
        return super()._move_autocomplete_invoice_lines_write(vals)
