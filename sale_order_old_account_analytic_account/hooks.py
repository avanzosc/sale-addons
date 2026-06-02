def _post_install_put_project_in_sale_orders(env):
    env.cr.execute("""
        SELECT order_id, analytic_account_id
        FROM sale_order_analytic_backup
    """)
    for order_id, analytic_id in env.cr.fetchall():
        env.cr.execute(
            """
             SELECT id
             FROM project_project
             WHERE account_id = %s
        """,
            (analytic_id,),
        )
        projects = env.cr.fetchall()
        if len(projects) == 1:
            env.cr.execute(
                """
                 UPDATE sale_order
                 SET project_id = %s,
                     old_account_analytic_account_id = %s
                 WHERE id = %s
            """,
                (projects[0][0], analytic_id, order_id),
            )
            env.cr.execute(
                """
                 UPDATE project_project
                 SET allow_billable = True
                 WHERE id = %s
            """,
                (projects[0][0],),
            )
        else:
            env.cr.execute(
                """
                 UPDATE sale_order
                 SET old_account_analytic_account_id = %s
                 WHERE id = %s
            """,
                (analytic_id, order_id),
            )
