# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_analytic_account aa
        SET user_id = (SELECT user_id
                         FROM sale_order so
                        WHERE so.analytic_account_id = aa.id
                          AND user_id IS NOT NULL
                       ORDER BY name LIMIT 1);
        """)
