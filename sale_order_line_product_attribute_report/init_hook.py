# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, SUPERUSER_ID
from ._common import _catch_top_bottom_graphic_info
import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Pre-creating column top_graphic for table sale_order_line")
    if not openupgrade.column_exists(cr, "sale_order_line", "top_graphic"):
        cr.execute(
            """
            ALTER TABLE sale_order_line
            ADD COLUMN top_graphic varchar;
            COMMENT ON COLUMN sale_order_line.top_graphic
            IS 'Top Graphic';
            """
        )
    _logger.info("Pre-creating column bottom_graphic for table sale_order_line")
    if not openupgrade.column_exists(cr, "sale_order_line", "bottom_graphic"):
        cr.execute(
            """
            ALTER TABLE sale_order_line
            ADD COLUMN bottom_graphic varchar;
            COMMENT ON COLUMN sale_order_line.bottom_graphic
            IS 'Bottom Graphic';
            """
        )
    sale_lines = env["sale.order.line"].search([])
    for sale_line in sale_lines:
        top_graphic, bottom_graphic = _catch_top_bottom_graphic_info(sale_line)
        top_graphic = top_graphic.replace("'", "''")
        bottom_graphic = bottom_graphic.replace("'", "''")
        cr.execute("""
            UPDATE sale_order_line
            SET top_graphic = '%s',
                bottom_graphic = '%s'
            WHERE id = %s;
        """ % (top_graphic, bottom_graphic, sale_line.id))
