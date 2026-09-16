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
    if not column_exists(cr, "sale_order_line", "delivered_amount"):
        create_column(cr, "sale_order_line", "delivered_amount", "numeric")
    if not column_exists(cr, "sale_order_line", "invoiced_amount"):
        create_column(cr, "sale_order_line", "invoiced_amount", "numeric")


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


def populate_sale_order_line_pending_delivery(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET
            qty_pending_delivery = CASE
                WHEN qty_delivered_method = 'stock_move'
                THEN GREATEST(COALESCE(product_uom_qty, 0) - COALESCE(qty_delivered, 0), 0)
                ELSE 0
            END,
            amount_pending_delivery = CASE
                WHEN qty_delivered_method = 'stock_move'
                THEN GREATEST(COALESCE(product_uom_qty, 0) - COALESCE(qty_delivered, 0), 0)
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
            qty_pending_invoicing = COALESCE(product_uom_qty, 0) - COALESCE(qty_invoiced, 0),
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


def populate_sale_order_line_delivered_invoiced_amounts(cr):
    cr.execute(
        """
        UPDATE sale_order_line
        SET
            delivered_amount = COALESCE(qty_delivered, 0)
                               * COALESCE(price_unit, 0)
                               * (1 - COALESCE(discount, 0) / 100),
            invoiced_amount = COALESCE(qty_invoiced, 0)
                              * COALESCE(price_unit, 0)
                              * (1 - COALESCE(discount, 0) / 100)
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


def _pre_init_sale_pending_info(cr):
    _logger.info("sale_line_pending_info: Starting pre-init hook")

    create_column_sale_order_line(cr)
    create_column_sale_order(cr)

    _logger.info("sale_line_pending_info: Pre-init completed successfully.")


def _post_init_sale_pending_info(cr, registry):
    _logger.info("sale_line_pending_info: Starting post-init hook")

    populate_sale_order_line_pending_delivery(cr)
    populate_sale_order_line_pending_invoicing(cr)
    populate_sale_order_line_shipped_pending_invoicing(cr)
    populate_sale_order_line_delivered_invoiced_amounts(cr)

    populate_sale_order_total_pending_delivery(cr)
    populate_sale_order_total_pending_invoicing(cr)
    populate_sale_order_total_shipped_pending_invoicing(cr)
    populate_sale_order_qty_ordered(cr)
    populate_sale_order_qty_delivered(cr)

    _logger.info("sale_line_pending_info: Post-init completed successfully.")
