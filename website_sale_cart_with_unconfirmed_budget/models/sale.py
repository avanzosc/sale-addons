# -*- coding: utf-8 -*-
from odoo import models, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        # Comprobar si hay un presupuesto sin confirmar
        unconfirmed_budget = self.env['sale.order'].search([
            ('state', '=', 'draft'),
            ('partner_id', '=', vals.get('partner_id')),
        ], limit=1)

        if unconfirmed_budget:
            # Si hay un presupuesto sin confirmar, cargar los productos en él
            unconfirmed_budget.order_line.unlink()  # Eliminar líneas de presupuesto existente
            for line in vals.get('order_line', []):
                unconfirmed_budget.order_line.create({
                    'order_id': unconfirmed_budget.id,
                    'product_id': line[2]['product_id'],
                    'product_uom_qty': line[2]['product_uom_qty'],
                })
            return unconfirmed_budget
        
        # Si no hay presupuesto sin confirmar, proceder con la creación normal
        return super(SaleOrder, self).create(vals)

class WebsiteSale(models.Model):
    _inherit = "website.sale"

    @api.model
    def cart_update(self, **kwargs):
        # Comprobar si se está agregando un producto al carrito
        product_id = kwargs.get('product_id')
        if product_id:
            # Comprobar si hay un presupuesto sin confirmar
            unconfirmed_budget = self.env['sale.order'].search([
                ('state', '=', 'draft'),
                ('partner_id', '=', self.env.user.partner_id.id),
            ], limit=1)

            if unconfirmed_budget:
                # Agregar el producto al presupuesto existente
                unconfirmed_budget.order_line.create({
                    'order_id': unconfirmed_budget.id,
                    'product_id': product_id,
                    'product_uom_qty': kwargs.get('add_qty', 1),
                })
                return {'message': _('Product added to the existing unconfirmed budget.')}

        # Proceder con la lógica de actualización del carrito normal
        return super(WebsiteSale, self).cart_update(**kwargs)
