from psycopg2.extensions import AsIs

from odoo import fields, models, tools


class ProductAttributeSaleReport(models.Model):
    _name = "product.attribute.sale.report"
    _description = "Product Attribute Sale Report"
    _auto = False
    _rec_name = "order_line_id"
    _order = "order_line_id,product_id,attribute_id"  # ,attribute_value_id"

    order_line_id = fields.Many2one("sale.order.line", "Order Line")
    date_order = fields.Datetime(string="Date")
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    attribute_id = fields.Many2one("product.attribute", "Product Attribute")
    attribute_value_id = fields.Many2one("product.attribute.value", "Attribute Value")
    product_uom_qty = fields.Float("Ordered Qty")

    def _select(self):
        select_str = """
                SELECT
                    row_number() OVER () as id,
                    ol.id AS order_line_id,
                    p.id AS product_id,
                    ptav.attribute_id AS attribute_id,
                    attv.id AS attribute_value_id,
                    ol.product_uom_qty AS product_uom_qty,
                    so.date_order AS date_order
            """
        return select_str

    def _from(self):
        from_str = """
                    FROM sale_order_line ol
                    JOIN sale_order as so ON so.id = ol.order_id
                    JOIN product_product as p ON p.id = ol.product_id
                    JOIN product_variant_combination pvc
                        ON pvc.product_product_id = p.id
                    JOIN product_template_attribute_value ptav
                        ON ptav.id = pvc.product_template_attribute_value_id
                    JOIN product_attribute att ON ptav.attribute_id = att.id
                    JOIN product_attribute_value attv
                        ON ptav.product_attribute_value_id = attv.id

            """
        return from_str

    def _where(self, condition=None):
        where = "WHERE so.date_order > CURRENT_DATE + INTERVAL '-3 month'"
        # if condition:
        #     where = where + 'WHERE '
        # if condition.get('year_select', None):
        #     today = date.today().year
        #     year_cond = condition.get('year_select')
        #     if year_cond == 'previous':
        #         today = today - 1
        #     if year_cond == 'next':
        #         today = today + 1
        #     where += "so.confirmation_date > '%s-01-01' " % today
        # if condition.get('catalog_id', None):
        #     if len(where) > 6:
        #         where += " AND "
        #     catalog_cond = condition.get('catalog_id')
        #     where += "so.catalog_id = %d " % catalog_cond
        # if condition.get('internal_product_category_id', None):
        #     if len(where) > 6:
        #         where += " AND "
        #     internal_c_cond = condition.get('internal_product_category_id')
        #     where += "p.internal_product_category_id = %d " % internal_c_cond
        # if condition.get('product_category_id', None):
        #     if len(where) > 6:
        #         where += " AND "
        #     category_cond = condition.get('product_category_id')
        #     where += "p.catalog_id = %d " % category_cond

        return where

    def _group_by(self):
        group_by_str = """
                GROUP BY ol.id, p.id, ptav.attribute_id, attv.id, so.date_order
             """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        condition = self._context.get("data")
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""",
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                AsIs(self._where(condition=condition)),
                AsIs(self._group_by()),
            ),
        )
