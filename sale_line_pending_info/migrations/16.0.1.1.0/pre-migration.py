# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Pre-creating column qty_ordered for table sale_order")
    if not openupgrade.column_exists(env.cr, "sale_order", "qty_ordered"):
        env.cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN qty_ordered float;
            COMMENT ON COLUMN sale_order.qty_ordered
            IS 'Units Ordered';
            """
        )
    _logger.info("Pre-creating column qty_delivered for table sale_order")
    if not openupgrade.column_exists(env.cr, "sale_order", "qty_delivered"):
        env.cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN qty_delivered float;
            COMMENT ON COLUMN sale_order.qty_delivered
            IS 'Units Delivered';
            """
        )
    _logger.info("Calculating column qty_ordered for table sale_order")
    if openupgrade.column_exists(env.cr, "sale_order", "qty_ordered"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE sale_order
            SET qty_ordered = (SELECT sum(sale_order_line.product_uom_qty)
                               FROM sale_order_line
                               WHERE sale_order_line.order_id = sale_order.id
                                 AND sale_order_line.state != 'cancel'
                              )
            """,
        )
    _logger.info("Calculating column qty_delivered for table sale_order")
    if openupgrade.column_exists(env.cr, "sale_order", "qty_delivered"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE sale_order
            SET qty_delivered = (SELECT sum(sale_order_line.qty_delivered)
                                 FROM sale_order_line
                                 WHERE sale_order_line.order_id = sale_order.id
                                   AND sale_order_line.state != 'cancel'
                                )
            """,
        )
