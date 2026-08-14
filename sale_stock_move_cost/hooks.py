import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def install_stock_move_line__cost(env):
    _logger.info("stock_move_cost: Setting price_unit_cost and cost for move lines")
    env.cr.execute(
        """
        WITH updated_lines AS (
            UPDATE stock_move_line ml
            SET price_unit_cost = CASE
                WHEN ml.lot_id IS NOT NULL THEN
                    (SELECT purchase_price FROM stock_lot l WHERE l.id = ml.lot_id)
                ELSE
                    COALESCE(
                        NULLIF(
                            (SELECT pol.price_unit
                             FROM purchase_order_line pol
                             JOIN purchase_order po ON po.id = pol.order_id
                             WHERE pol.product_id = ml.product_id
                               AND pol.state IN ('purchase', 'done')
                             ORDER BY po.date_order DESC, pol.id DESC
                             LIMIT 1),
                            0),
                        (SELECT (pp.standard_price ->> ml.company_id::text)::numeric
                         FROM product_product pp
                         WHERE pp.id = ml.product_id),
                        0)
            END
            WHERE ml.lot_id IS NOT NULL
               OR (ml.lot_id IS NULL AND ml.product_id IS NOT NULL)
            RETURNING id, price_unit_cost, quantity
        )
        UPDATE stock_move_line ml
        SET cost = ul.price_unit_cost * ul.quantity
        FROM updated_lines ul
        WHERE ml.id = ul.id
          AND ul.price_unit_cost > 0
          AND ul.quantity > 0;
        """
    )


def install_stock_move__cost(env):
    _logger.info(
        "stock_move_cost: Calculating cost and price_unit_cost for stock moves"
    )
    env.cr.execute(
        """
        UPDATE stock_move sm
        SET cost = sub.total_cost,
            price_unit_cost = CASE
                WHEN sub.total_cost > 0 AND sm.quantity > 0
                THEN sub.total_cost / sm.quantity
                ELSE 0
            END
        FROM (
            SELECT move_id, SUM(cost) as total_cost
            FROM stock_move_line
            GROUP BY move_id
        ) sub
        WHERE sm.id = sub.move_id;
        """
    )


def _pre_init_sale_stock_move_cost(env):
    _logger.info("sale_stock_move_cost: Starting pre-init hook")

    if not column_exists(env.cr, "sale_order_line", "sale_line_cost"):
        create_column(env.cr, "sale_order_line", "sale_line_cost", "numeric")
    if not column_exists(env.cr, "sale_order_line", "sale_line_margin"):
        create_column(env.cr, "sale_order_line", "sale_line_margin", "numeric")
    if not column_exists(env.cr, "sale_order", "sale_order_cost"):
        create_column(env.cr, "sale_order", "sale_order_cost", "numeric")
    if not column_exists(env.cr, "sale_order", "sale_order_margin"):
        create_column(env.cr, "sale_order", "sale_order_margin", "numeric")

    # install_stock_move_line__cost(env)
    # install_stock_move__cost(env)
    _logger.info("sale_stock_move_cost: Pre-init hook completed")


def _post_init_sale_stock_move_cost(env):
    _logger.info("sale_stock_move_cost: Starting post-init hook")
    env.cr.execute(
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
    env.cr.execute(
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
    env.cr.execute(
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
    env.cr.execute(
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
