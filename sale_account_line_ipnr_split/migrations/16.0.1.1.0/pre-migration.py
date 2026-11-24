# Copyright 2026 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging

from psycopg2 import sql

from odoo.tools.sql import column_exists, create_column

_logger = logging.getLogger(__name__)

# (table, old column, new column, SQL type)
FIELDS_TO_RENAME = [
    (
        "account_move_line",
        "x_ipnr_gross_price_unit",
        "ipnr_gross_price_unit",
        "numeric",
    ),
    ("account_move_line", "x_ipnr_parent_line_id", "ipnr_parent_line_id", "int4"),
    ("sale_order_line", "x_ipnr_gross_price_unit", "ipnr_gross_price_unit", "numeric"),
    ("sale_order_line", "x_ipnr_parent_line_id", "ipnr_parent_line_id", "int4"),
    ("res_config_settings", "x_ipnr_product_id", "ipnr_product_id", "int4"),
    ("res_config_settings", "x_ipnr_rounding_digits", "ipnr_rounding_digits", "int4"),
]


def migrate(cr, version):
    if not version:
        return
    for table, old_column, new_column, column_type in FIELDS_TO_RENAME:
        if not column_exists(cr, table, new_column):
            _logger.info("Creating column %s.%s", table, new_column)
            create_column(cr, table, new_column, column_type)
        if column_exists(cr, table, old_column):
            _logger.info(
                "Copying values from %s.%s to %s.%s",
                table,
                old_column,
                table,
                new_column,
            )
            cr.execute(
                sql.SQL(
                    """
                    UPDATE {table}
                       SET {new_column} = {old_column}
                     WHERE {old_column} IS NOT NULL
                    """
                ).format(
                    table=sql.Identifier(table),
                    new_column=sql.Identifier(new_column),
                    old_column=sql.Identifier(old_column),
                )
            )
    _keep_old_fields(cr)


def _keep_old_fields(cr):
    """Protect the old fields (x_...) so Odoo does not remove them.

    At the end of the update, Odoo deletes the ir.model.fields records whose
    XML-ID belongs to the module, are not flagged as noupdate and are no
    longer defined in code, and that drops their columns. Flagging those
    XML-IDs as noupdate keeps everything (XML-IDs, ir.model.fields records
    and columns with their data) in the database. Nothing is deleted here.
    """
    xmlids = [
        "field_{}__{}".format(table, old_column)
        for table, old_column, _new_column, _column_type in FIELDS_TO_RENAME
    ]
    cr.execute(
        """
        UPDATE ir_model_data
           SET noupdate = TRUE
         WHERE module = 'sale_account_line_ipnr_split'
           AND model = 'ir.model.fields'
           AND name IN %s
        """,
        (tuple(xmlids),),
    )
    _logger.info(
        "Flagged %s old field XML-IDs as noupdate, the old fields are kept",
        cr.rowcount,
    )
