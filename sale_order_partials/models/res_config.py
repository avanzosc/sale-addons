# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    sale_type_id = fields.Many2one(comodel_name='sale.order.type',
                                   string="Partial orders type")

    def _get_parameter(self, key, default=False):
        param_obj = self.env['ir.config_parameter']
        rec = param_obj.search([('key', '=', key)])
        return rec or default

    def _write_or_create_param(self, key, value):
        param_obj = self.env['ir.config_parameter']
        rec = self._get_parameter(key)
        if rec:
            if not value:
                rec.unlink()
            else:
                rec.value = value
        elif value:
            param_obj.create({'key': key, 'value': value})

    @api.multi
    def get_default_parameters(self):
        def get_value(key, default=''):
            rec = self._get_parameter(key)
            return rec and rec.value or default
        return {
            'sale_type_id': get_value('sale.type.id', False),
        }

    @api.multi
    def set_parameters(self):
        self._write_or_create_param('sale.type.id', self.sale_type_id.id)
