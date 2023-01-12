# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        SELECT id, sales_goal_monthly, sales_goal_yearly
          FROM res_partner
        WHERE sales_goal_yearly IS NOT NULL OR sales_goal_monthly IS NOT NULL;
        """)
    for partner_id, monthly, yearly in cr.fetchall():
        if monthly:
            cr.execute(
                """
                UPDATE sale_order_line l
                SET sales_goal_monthly_percentage = (
                    price_subtotal * 100 / %f
                )
                WHERE price_subtotal != 0.0 AND order_partner_id = %d;""" %
                (monthly, partner_id))
        if yearly:
            cr.execute(
                """
                UPDATE sale_order_line l
                SET sales_goal_yearly_percentage = (
                    price_subtotal * 100 / %f
                )
                WHERE price_subtotal != 0.0 AND order_partner_id = %d;""" %
                (yearly, partner_id))
