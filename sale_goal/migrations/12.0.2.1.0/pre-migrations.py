# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.column_exists(cr, "res_users", "sales_goal_yearly"):
        openupgrade.logged_query(
            cr,
            """
            ALTER TABLE res_users
            ADD COLUMN sales_goal_yearly numeric;
            """,
        )

    if not openupgrade.column_exists(cr, "res_users", "sales_goal_monthly"):
        openupgrade.logged_query(
            cr,
            """
            ALTER TABLE res_users
            ADD COLUMN sales_goal_monthly numeric;
            """,
        )
