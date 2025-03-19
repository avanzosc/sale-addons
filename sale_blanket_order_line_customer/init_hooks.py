# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column customer_id for table sale_blanket_order_line")
    if not openupgrade.column_exists(cr, "sale_blanket_order_line", "customer_id"):
        cr.execute(
            """
            ALTER TABLE sale_blanket_order_line
            ADD COLUMN customer_id integer;
            COMMENT ON COLUMN sale_blanket_order_line.customer_id
            IS 'Customer';
            """
        )

    _logger.info("Pre-computing column customer_id for table sale_blanket_order_line")
    cr.execute(
        """
        UPDATE sale_blanket_order_line
        set    customer_id = (
               SELECT sale_blanket_order.partner_id
               FROM   sale_blanket_order
               WHERE  sale_blanket_order.id = sale_blanket_order_line.order_id
               )
        WHERE  order_id is not null
    """
    )
