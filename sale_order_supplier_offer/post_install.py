# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def purchase_order_with_sale_order(env):
    sale_orders = env["sale.order"].search([])
    for sale_order in sale_orders:
        cond = [("origin", "=", sale_order.name)]
        purchase = env["purchase.order"].search(cond, limit=1)
        if purchase:
            purchase.sale_order_id = sale_order.id
