# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _prepare_move_default_values(self, return_line, new_picking):
        vals = super(ReturnPicking, self)._prepare_move_default_values(
            return_line, new_picking)
        vals.update({
            'date_expected': fields.Datetime.to_datetime(
                self.picking_id.sale_id.expected_end_date),
        })
        return vals
