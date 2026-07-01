
from odoo import fields, models, tools
from psycopg2.extensions import AsIs


class ProductAttributeCatalogReport(models.Model):
    _name = 'product.attribute.catalog.report'
    _description = 'Product Attribute Catalog Report'
    _auto = False
    _rec_name = "catalog_id"
    _order = "catalog_id,product_id,attribute_id,attribute_value_id"

    catalog_id = fields.Many2one(
        'product.catalog.web', 'Catalogue')
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product")
    attribute_id = fields.Many2one(
        'product.attribute', 'Product Attribute')
    attribute_value_id = fields.Many2one(
        'product.attribute.value', 'Attribute Value')

    def _select(self):
        select_str = """
                SELECT
                    row_number() OVER () as id,
                    c.id AS catalog_id,
                    p.id AS product_id,
                    ptav.attribute_id AS attribute_id,
                    attv.id AS attribute_value_id
            """
        return select_str

    def _from(self):
        from_str = """
                    FROM product_catalog_web c
                    JOIN catalog_web_product_template_rel as cwptr
                        ON c.id = cwptr.catalog_id
                    JOIN product_template as pt ON pt.id = cwptr.product_tmpl_id
                    JOIN product_product as p ON p.product_tmpl_id = pt.id
                    JOIN product_variant_combination pvc
                        ON pvc.product_product_id = p.id
                    JOIN product_template_attribute_value ptav
                        ON ptav.id = pvc.product_template_attribute_value_id
                    JOIN product_attribute att ON ptav.attribute_id = att.id
                    JOIN product_attribute_value attv
                        ON ptav.product_attribute_value_id = attv.id
             
            """
        return from_str

    def _where(self, catalog_id=None):
        return "WHERE c.visible_slider = true"

    def _group_by(self):
        group_by_str = """
                GROUP BY c.id, p.id, ptav.attribute_id, attv.id
                LIMIT 10000
             """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        catalog_id = self._context.get('catalog_id')
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""", (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                AsIs(self._where(catalog_id=catalog_id)),
                AsIs(self._group_by()),
            ),
        )
