# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        result = super(SaleOrderLine, self)._onchange_product_uom_qty()
        if "warning" in result:
            result["warning"] = []
        return result

    def write(self, values):
        lines = self.env['sale.order.line']
        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            lines = self.filtered(
                lambda r: r.state == 'sale' and not r.is_expense and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) == 1)
        previous_product_uom_qty = {line.id: line.product_uom_qty for line in lines}
        res = super(SaleOrderLine, self).write(values)
        if lines:
            lines._action_launch_stock_rule(previous_product_uom_qty)
        return res

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        result = super(SaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty=previous_product_uom_qty)
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            line = line.with_company(line.company_id)
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if line.state == 'sale' and line.product_id.type in ('consu','product') and float_compare(qty, line.product_uom_qty, precision_digits=precision) > 0:
                group_id = line._get_procurement_group()
                if not group_id:
                    group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                    line.order_id.procurement_group_id = group_id
                else:
                    updated_vals = {}
                    if group_id.partner_id != line.order_id.partner_shipping_id:
                        updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                    if group_id.move_type != line.order_id.picking_policy:
                        updated_vals.update({'move_type': line.order_id.picking_policy})
                    if updated_vals:
                        group_id.write(updated_vals)
                        
                values = line._prepare_procurement_values(group_id=group_id)
                product_qty = line.product_uom_qty - qty
                
                line_uom = line.product_uom
                quant_uom = line.product_id.uom_id
                product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
                procurements.append(self.env['procurement.group'].Procurement(
                    line.product_id, product_qty, procurement_uom,
                    line.order_id.partner_shipping_id.property_stock_customer,
                    line.product_id.display_name, line.order_id.name, line.order_id.company_id, values))
                if procurements:
                    self.env['procurement.group'].run(procurements)
        return result
