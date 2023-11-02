# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        """
        UPDATE sale_order_line
        set    product_packaging = product_packaging_id
    """
    )
    cr.execute(
        """
        ALTER TABLE sale_order_line DROP COLUMN product_packaging_id
    """
    )
