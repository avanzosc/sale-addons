# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.column_exists(
        cr,
        "sale_order_line",
        "sales_goal_yearly_percentage"
    ):
        openupgrade.logged_query(
            cr,
            """
            ALTER TABLE sale_order_line
            ADD COLUMN sales_goal_yearly_percentage numeric;
            """)

    if not openupgrade.column_exists(
        cr,
        "sale_order_line",
        "sales_goal_monthly_percentage"
    ):
        openupgrade.logged_query(
            cr,
            """
            ALTER TABLE sale_order_line
            ADD COLUMN sales_goal_monthly_percentage numeric;
            """)
