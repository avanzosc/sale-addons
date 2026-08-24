# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from psycopg2 import sql as psql

_logger = logging.getLogger(__name__)

_CATALOG_COLUMNS = [
    "id",
    "company_id",
    "warehouse_id",
    "create_uid",
    "write_uid",
    "name",
    "inventory_availability",
    "description",
    "active",
    "logo",
    "create_date",
    "write_date",
]


def _table_exists(cr, name):
    cr.execute(
        "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
        (name,),
    )
    return cr.fetchone()[0]


def _columns_in_table(cr, table, wanted):
    cr.execute(
        """
        SELECT column_name
          FROM information_schema.columns
         WHERE table_name   = %s
           AND column_name  = ANY(%s)
         ORDER BY ordinal_position
        """,
        (table, list(wanted)),
    )
    return [row[0] for row in cr.fetchall()]


def _drop_fks_to_table(cr, referenced_table):
    """Drop every FK constraint that points to *referenced_table*."""
    cr.execute(
        """
        SELECT tc.constraint_name, tc.table_name
          FROM information_schema.table_constraints  tc
          JOIN information_schema.referential_constraints rc
               ON rc.constraint_name = tc.constraint_name
          JOIN information_schema.table_constraints  rc2
               ON rc2.constraint_name = rc.unique_constraint_name
         WHERE rc2.table_name = %s
           AND tc.constraint_type = 'FOREIGN KEY'
        """,
        (referenced_table,),
    )
    for constraint, table in cr.fetchall():
        _logger.info(
            "sale_product_catalog: dropping FK %s on %s -> %s",
            constraint,
            table,
            referenced_table,
        )
        cr.execute(
            psql.SQL("ALTER TABLE {} DROP CONSTRAINT IF EXISTS {}").format(
                psql.Identifier(table),
                psql.Identifier(constraint),
            )
        )


def pre_init_hook(env):
    cr = env.cr

    if not _table_exists(cr, "product_catalog_web"):
        return

    if _table_exists(cr, "product_catalog"):
        _logger.warning(
            "sale_product_catalog: product_catalog already exists — "
            "skipping v12 data migration."
        )
        return

    _drop_fks_to_table(cr, "product_catalog_web")
    cols = _columns_in_table(cr, "product_catalog_web", _CATALOG_COLUMNS)
    col_sql = psql.SQL(", ").join(psql.Identifier(c) for c in cols)

    cr.execute(
        psql.SQL(
            "CREATE TABLE product_catalog AS SELECT {cols} FROM product_catalog_web"
        ).format(cols=col_sql)
    )
    cr.execute("ALTER TABLE product_catalog ADD PRIMARY KEY (id)")
    cr.execute("CREATE SEQUENCE IF NOT EXISTS product_catalog_id_seq")
    cr.execute(
        "SELECT setval('product_catalog_id_seq', "
        "COALESCE((SELECT MAX(id) FROM product_catalog), 1))"
    )
    cr.execute(
        "ALTER TABLE product_catalog ALTER COLUMN id "
        "SET DEFAULT nextval('product_catalog_id_seq'::regclass)"
    )
    _logger.info(
        "sale_product_catalog: created product_catalog from product_catalog_web "
        "(columns: %s)",
        ", ".join(cols),
    )


def post_init_hook(env):
    cr = env.cr

    cr.execute(
        """
        UPDATE product_pricelist_item pli
           SET product_tmpl_id = pp.product_tmpl_id,
               applied_on      = '0_product_variant'
          FROM product_product pp
         WHERE pli.product_id      = pp.id
           AND pli.product_id      IS NOT NULL
           AND pli.product_tmpl_id IS NULL
        """
    )
    _logger.info(
        "sale_product_catalog: filled product_tmpl_id for %d variant-level "
        "pricelist items (v12 migration fix)",
        cr.rowcount,
    )

    if not _table_exists(cr, "catalog_web_product_pricelist_rel"):
        return
    if not _table_exists(cr, "catalog_web_product_template_rel"):
        _logger.warning(
            "sale_product_catalog: catalog_web_product_template_rel not found — "
            "skipping pricelist item migration."
        )
        return

    cr.execute(
        """
        INSERT INTO pricelist_item_catalog_rel (pricelist_item_id, catalog_id)
        SELECT DISTINCT pli.id, cwpl.catalog_id
          FROM product_pricelist_item pli
          JOIN catalog_web_product_pricelist_rel cwpl
               ON cwpl.pricelist_id = pli.pricelist_id
          JOIN catalog_web_product_template_rel cwpt
               ON cwpt.catalog_id    = cwpl.catalog_id
              AND cwpt.product_tmpl_id = pli.product_tmpl_id
         WHERE pli.product_tmpl_id IS NOT NULL
           AND pli.product_id IS NULL
        ON CONFLICT DO NOTHING
        """
    )
    _logger.info(
        "sale_product_catalog: migrated %d product-level item→catalog links from v12",
        cr.rowcount,
    )

    cr.execute(
        """
        INSERT INTO pricelist_item_catalog_rel (pricelist_item_id, catalog_id)
        SELECT DISTINCT pli.id, cwpl.catalog_id
          FROM product_pricelist_item pli
          JOIN product_product pp
               ON pp.id = pli.product_id
          JOIN catalog_web_product_pricelist_rel cwpl
               ON cwpl.pricelist_id = pli.pricelist_id
          JOIN catalog_web_product_template_rel cwpt
               ON cwpt.catalog_id    = cwpl.catalog_id
              AND cwpt.product_tmpl_id = pp.product_tmpl_id
         WHERE pli.product_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """
    )
    _logger.info(
        "sale_product_catalog: migrated %d variant-level item→catalog links from v12",
        cr.rowcount,
    )
