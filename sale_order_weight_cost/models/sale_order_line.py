# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Float(
        string='Weight', digits=dp.get_precision('Stock Weight'))
    weight_uom_id = fields.Many2one(
        comodel_name='uom.uom', string='Weight Unit of Measure',
        compute='_compute_weight_uom_id')
    weight_uom_name = fields.Char(
        string='Weight unit of measure label', related='weight_uom_id.name',
        readonly=True)
    volume = fields.Float(string='Volume', help="The volume in m3.")
    cost = fields.Float(
        string='Cost', digits=dp.get_precision('Product Price'))

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        self.weight = self.product_id.weight
        self.cost = self.product_id.standard_price
        self.volume = self.product_id.volume
        return res

    @api.multi
    def _compute_weight_uom_id(self):
        tmpl_obj = self.env['product.template']
        weight_uom_id = tmpl_obj._get_weight_uom_id_from_ir_config_parameter()
        for line in self:
            line.weight_uom_id = weight_uom_id
