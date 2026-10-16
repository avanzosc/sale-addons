import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def _pre_init_sale_stock_move_cost(cr):
    _logger.info("sale_stock_move_cost: Starting pre-init hook")
    if not column_exists(cr, "sale_order_line", "sale_line_cost"):
        create_column(cr, "sale_order_line", "sale_line_cost", "numeric")
    if not column_exists(cr, "sale_order_line", "sale_line_margin"):
        create_column(cr, "sale_order_line", "sale_line_margin", "numeric")
    if not column_exists(cr, "sale_order", "sale_order_cost"):
        create_column(cr, "sale_order", "sale_order_cost", "numeric")
    if not column_exists(cr, "sale_order", "sale_order_margin"):
        create_column(cr, "sale_order", "sale_order_margin", "numeric")
    _logger.info("sale_stock_move_cost: Pre-init hook completed")


def _post_init_sale_stock_move_cost(cr, registry):
    _logger.info("sale_stock_move_cost: Starting post-init hook")
    cr.execute(
        """
        UPDATE sale_order_line sol
        SET sale_line_cost = COALESCE(sub.cost, 0)
        FROM (
            SELECT sm.sale_line_id, SUM(sml.cost) as cost
            FROM stock_move sm
            JOIN stock_move_line sml ON sml.move_id = sm.id
            WHERE sm.state != 'cancel'
            GROUP BY sm.sale_line_id
        ) sub
        WHERE sol.id = sub.sale_line_id
        """
    )
    cr.execute(
        """
        UPDATE sale_order_line
        SET sale_line_margin = CASE
            WHEN sale_line_cost > 0
            THEN price_subtotal - sale_line_cost
            ELSE 0
        END
        WHERE sale_line_cost > 0
        """
    )
    cr.execute(
        """
        UPDATE sale_order so
        SET sale_order_cost = COALESCE(sub.total_cost, 0)
        FROM (
            SELECT order_id, SUM(sale_line_cost) as total_cost
            FROM sale_order_line
            WHERE sale_line_cost > 0
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
        """
    )
    cr.execute(
        """
        UPDATE sale_order so
        SET sale_order_margin = COALESCE(sub.total_margin, 0)
        FROM (
            SELECT order_id, SUM(sale_line_margin) as total_margin
            FROM sale_order_line
            WHERE sale_line_cost > 0
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
        """
    )
    _logger.info("sale_stock_move_cost: Post-init hook completed")
