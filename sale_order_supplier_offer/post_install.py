# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import SUPERUSER_ID, api


def purchase_order_with_sale_order(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        sale_orders = env["sale.order"].search([])
        for sale_order in sale_orders:
            cond = [("origin", "=", sale_order.name)]
            purchase = env["purchase.order"].search(cond, limit=1)
            if purchase:
                purchase.sale_order_id = sale_order.id
    return
