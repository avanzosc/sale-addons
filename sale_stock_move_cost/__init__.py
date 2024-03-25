from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_cost_in_sales(cr, registry):
    cr.execute(
        """
        UPDATE sale_order
        SET manufacturing_order_cost = (select sum(of.cost)
                                        from mrp_production of
                                        where of.sale_id = sale_order.id)
        """
    )
    cr.execute(
        """
        UPDATE sale_order
        SET sale_margin_with_manufacturing_order = amount_untaxed - manufacturing_order_cost
        where manufacturing_order_cost > 0
        """
    )