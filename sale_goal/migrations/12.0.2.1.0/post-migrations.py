# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    user_obj = env["res.users"]
    partner_obj = env["res.partner"]
    users = user_obj.search([], order="id")
    for user_id in users.ids:
        partners = partner_obj.search(
            [
                ("user_id", "=", user_id),
            ]
        )
        sales_goal_monthly = 0.0
        sales_goal_yearly = 0.0
        if partners:
            sales_goal_monthly = sum(partners.mapped("sales_goal_monthly"))
            sales_goal_yearly = sum(partners.mapped("sales_goal_yearly"))
        cr.execute(
            """
            UPDATE res_users
            SET sales_goal_monthly = %s,
                sales_goal_yearly = %s
            WHERE id = %s;
            """,
            (
                sales_goal_monthly,
                sales_goal_yearly,
                user_id,
            ),
        )
