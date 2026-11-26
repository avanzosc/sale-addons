import logging

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)


def create_column_sale_order_line(cr):
    if not column_exists(cr, "sale_order_line", "qty_pending_delivery"):
        create_column(cr, "sale_order_line", "qty_pending_delivery", "numeric")
    if not column_exists(cr, "sale_order_line", "amount_pending_delivery"):
        create_column(cr, "sale_order_line", "amount_pending_delivery", "numeric")
    if not column_exists(cr, "sale_order_line", "qty_pending_invoicing"):
        create_column(cr, "sale_order_line", "qty_pending_invoicing", "numeric")
    if not column_exists(cr, "sale_order_line", "amount_pending_invoicing"):
        create_column(cr, "sale_order_line", "amount_pending_invoicing", "numeric")
    if not column_exists(cr, "sale_order_line", "qty_shipped_pending_invoicing"):
        create_column(cr, "sale_order_line", "qty_shipped_pending_invoicing", "numeric")
    if not column_exists(cr, "sale_order_line", "amount_shipped_pending_invoicing"):
        create_column(
            cr, "sale_order_line", "amount_shipped_pending_invoicing", "numeric"
        )
    if not column_exists(cr, "sale_order_line", "shipped_rate"):
        create_column(cr, "sale_order_line", "shipped_rate", "numeric")


def create_column_sale_order(cr):
    if not column_exists(cr, "sale_order", "total_qty_pending_delivery"):
        create_column(cr, "sale_order", "total_qty_pending_delivery", "numeric")
    if not column_exists(cr, "sale_order", "total_amount_pending_delivery"):
        create_column(cr, "sale_order", "total_amount_pending_delivery", "numeric")
    if not column_exists(cr, "sale_order", "total_qty_pending_invoicing"):
        create_column(cr, "sale_order", "total_qty_pending_invoicing", "numeric")
    if not column_exists(cr, "sale_order", "total_amount_pending_invoicing"):
        create_column(cr, "sale_order", "total_amount_pending_invoicing", "numeric")
    if not column_exists(cr, "sale_order", "total_qty_shipped_pending_invoicing"):
        create_column(
            cr, "sale_order", "total_qty_shipped_pending_invoicing", "numeric"
        )
    if not column_exists(cr, "sale_order", "total_amount_shipped_pending_invoicing"):
        create_column(
            cr, "sale_order", "total_amount_shipped_pending_invoicing", "numeric"
        )
    if not column_exists(cr, "sale_order", "qty_ordered"):
        create_column(cr, "sale_order", "qty_ordered", "numeric")
    if not column_exists(cr, "sale_order", "qty_delivered"):
        create_column(cr, "sale_order", "qty_delivered", "numeric")
    if not column_exists(cr, "sale_order", "shipped_rate"):
        create_column(cr, "sale_order", "shipped_rate", "numeric")


def populate_sale_order_line_pending_delivery(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET
            qty_pending_delivery = CASE
                WHEN qty_delivered_method = 'stock_move'
                THEN GREATEST(COALESCE(product_uom_qty, 0)
                    - COALESCE(qty_delivered, 0), 0)
                ELSE 0
            END,
            amount_pending_delivery = CASE
                WHEN qty_delivered_method = 'stock_move'
                THEN GREATEST(COALESCE(product_uom_qty, 0)
                    - COALESCE(qty_delivered, 0), 0)
                     * COALESCE(price_unit, 0)
                     * (1 - COALESCE(discount, 0) / 100)
                ELSE 0
            END
    """
    )


def populate_sale_order_line_pending_invoicing(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET
            qty_pending_invoicing = COALESCE(product_uom_qty, 0)
                                    - COALESCE(qty_invoiced, 0),
            amount_pending_invoicing = (COALESCE(product_uom_qty, 0) -
                                            COALESCE(qty_invoiced, 0))
                                       * COALESCE(price_unit, 0)
                                       * (1 - COALESCE(discount, 0) / 100)
    """
    )


def populate_sale_order_line_shipped_pending_invoicing(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET
            qty_shipped_pending_invoicing = GREATEST(COALESCE(qty_delivered, 0) -
                        COALESCE(qty_invoiced, 0), 0),
            amount_shipped_pending_invoicing = CASE
                WHEN COALESCE(qty_delivered, 0) - COALESCE(qty_invoiced, 0) > 0
                THEN (COALESCE(qty_delivered, 0) - COALESCE(qty_invoiced, 0))
                     * COALESCE(price_unit, 0)
                     * (1 - COALESCE(discount, 0) / 100)
                ELSE 0
            END
    """
    )


def populate_sale_order_line_shipped_rate(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET shipped_rate = CASE
            WHEN COALESCE(product_uom_qty, 0) != 0
            THEN (COALESCE(qty_delivered, 0) / product_uom_qty) * 100
            ELSE 0
        END
    """
    )


def populate_sale_order_total_pending_delivery(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET
            total_qty_pending_delivery = sub.total_qty,
            total_amount_pending_delivery = sub.total_amount
        FROM (
            SELECT
                order_id,
                SUM(qty_pending_delivery) AS total_qty,
                SUM(amount_pending_delivery) AS total_amount
            FROM sale_order_line
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def populate_sale_order_total_pending_invoicing(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET
            total_qty_pending_invoicing = sub.total_qty,
            total_amount_pending_invoicing = sub.total_amount
        FROM (
            SELECT
                order_id,
                SUM(qty_pending_invoicing) AS total_qty,
                SUM(amount_pending_invoicing) AS total_amount
            FROM sale_order_line
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def populate_sale_order_total_shipped_pending_invoicing(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET
            total_qty_shipped_pending_invoicing = sub.total_qty,
            total_amount_shipped_pending_invoicing = sub.total_amount
        FROM (
            SELECT
                order_id,
                SUM(qty_shipped_pending_invoicing) AS total_qty,
                SUM(amount_shipped_pending_invoicing) AS total_amount
            FROM sale_order_line
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def populate_sale_order_qty_ordered(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET qty_ordered = sub.total_qty
        FROM (
            SELECT
                order_id,
                SUM(product_uom_qty) AS total_qty
            FROM sale_order_line
            WHERE state != 'cancel'
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def populate_sale_order_qty_delivered(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET qty_delivered = sub.total_qty
        FROM (
            SELECT
                order_id,
                SUM(qty_delivered) AS total_qty
            FROM sale_order_line
            WHERE state != 'cancel'
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def populate_sale_order_shipped_rate(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET shipped_rate = sub.shipped_rate
        FROM (
            SELECT
                order_id,
                CASE
                    WHEN SUM(product_uom_qty) != 0
                    THEN (SUM(qty_delivered) / SUM(product_uom_qty)) * 100
                    ELSE 0
                END AS shipped_rate
            FROM sale_order_line
            WHERE state != 'cancel'
              AND product_uom_qty IS NOT NULL
            GROUP BY order_id
        ) sub
        WHERE so.id = sub.order_id
    """
    )


def _pre_init_sale_pending_info(env):
    _logger.info("sale_line_pending_info: Starting pre-init hook")

    create_column_sale_order_line(env.cr)
    create_column_sale_order(env.cr)

    _logger.info("sale_line_pending_info: Pre-init completed successfully.")


def _post_init_sale_pending_info(env):
    _logger.info("sale_line_pending_info: Starting post-init hook")

    populate_sale_order_line_pending_delivery(env.cr)
    populate_sale_order_line_pending_invoicing(env.cr)
    populate_sale_order_line_shipped_pending_invoicing(env.cr)
    populate_sale_order_line_shipped_rate(env.cr)

    populate_sale_order_total_pending_delivery(env.cr)
    populate_sale_order_total_pending_invoicing(env.cr)
    populate_sale_order_total_shipped_pending_invoicing(env.cr)
    populate_sale_order_qty_ordered(env.cr)
    populate_sale_order_qty_delivered(env.cr)
    populate_sale_order_shipped_rate(env.cr)

    _logger.info("sale_line_pending_info: Post-init completed successfully.")
