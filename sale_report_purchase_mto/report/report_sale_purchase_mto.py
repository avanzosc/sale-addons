# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, tools


class ReportSalePurchaseMTO(models.Model):

    _name = 'report.sale.purchase.mto'
    _auto = False

    sale_move_id = fields.Many2one(comodel_name='stock.move',
                                   string='Sale Move')
    sale_line_id = fields.Many2one(comodel_name='sale.order.line',
                                   string='Sale Line')
    sale_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    sale_picking_id = fields.Many2one(comodel_name='stock.picking',
                                      string='Sale Picking')
    purchase_move_id = fields.Many2one(comodel_name='stock.move',
                                       string='Purchase Move')
    purchase_line_id = fields.Many2one(comodel_name='purchase.order.line',
                                       string='Purchase Line')
    purchase_id = fields.Many2one(comodel_name='purchase.order',
                                  string='Purchase Order')
    purchase_picking_id = fields.Many2one(comodel_name='stock.picking',
                                          string='Purchase Picking')
    sale_date = fields.Date(string='Sale Confirm Date')
    sale_user_id = fields.Many2one(comodel_name='res.users',
                                   string='Sale Staff')
    sale_partner_id = fields.Many2one(comodel_name='res.partner',
                                      string='Customer')
    purchase_date = fields.Date(string='Purchase Date')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    purchase_partner_id = fields.Many2one(comodel_name='res.partner',
                                          string='Supplier')
    qty = fields.Float(string='Quantity')
    purchase_reception_date = fields.Date(string='Purchase Reception Date')
    purchase_date_done = fields.Date(string='Shipment Date')
    purchase_incoterm_id = fields.Many2one(comodel_name='stock.incoterms',
                                           string='Purchase Incoterm')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_sale_purchase_mto')
        cr.execute("""
            create or replace view report_sale_purchase_mto as (
            select
                sm.id as id,
                sm.id as sale_move_id,
                sol.id as sale_line_id,
                sol.order_id as sale_id,
                sm.picking_id as sale_picking_id,
                psm.id as purchase_move_id,
                pol.id as purchase_line_id,
                pol.order_id as purchase_id,
                psm.picking_id as purchase_picking_id,
                so.date_order as sale_date,
                so.user_id as sale_user_id,
                so.partner_id as sale_partner_id,
                po.date_order as purchase_date,
                sm.product_id as product_id,
                po.partner_id as purchase_partner_id,
                pol.product_qty as qty,
                po.incoterm_id as purchase_incoterm_id,
                psp.date_done as purchase_date_done,
                pol.date_planned as purchase_reception_date
            from
                stock_move sm
                left join procurement_order proc on proc.id=sm.procurement_id
                left join sale_order_line sol on sol.id=proc.sale_line_id
                left join sale_order so on so.id=sol.order_id
                left join stock_move psm on psm.move_dest_id=sm.id
                left join purchase_order_line pol on
                pol.id=psm.purchase_line_id
                left join purchase_order po on po.id = pol.order_id
                left join stock_picking psp on psp.id=psm.picking_id
            where
                sm.procurement_id is not null and
                proc.sale_line_id is not null and
                psm.move_dest_id is not null and
                psm.purchase_line_id is not null and
                so.state in ('progress', 'manual', 'shipping_except',
                             'invoice_except')
            ) """)
