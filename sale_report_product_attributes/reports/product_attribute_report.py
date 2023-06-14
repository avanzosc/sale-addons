
from odoo import tools
from odoo import api, fields, models
from psycopg2.extensions import AsIs


class ProductAttributeSaleReport(models.Model):
    _name = 'product.attribute.sale.report'
    _description = 'Product Attribute Sale Report'
    _auto = False
    _rec_name = "order_line_id"
    _order = "order_line_id,product_id,attribute_id" #,attribute_value_id"

    order_line_id = fields.Many2one(
        'sale.order.line', 'Order Line')
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product")
    attribute_id = fields.Many2one(
        'product.attribute', 'Product Attribute')
    # attribute_value_id = fields.Many2one(
    #     'product.attribute.value', 'Attribute Value')
    product_uom_qty = fields.Float('Ordered Qty')

    def _select(self):
        select_str = """
                SELECT
                    row_number() OVER () as id,
                    ol.id AS order_line_id,
                    p.id AS product_id,
                    ptal.attribute_id AS attribute_id,
                    ol.product_uom_qty AS product_uom_qty
            """
        return select_str

    def _from(self):
        from_str = """
                    FROM sale_order_line ol
                    JOIN sale_order as so ON so.id = ol.order_id
                    JOIN product_product as p ON p.id = ol.product_id
                    JOIN product_template as pt ON pt.id = p.product_tmpl_id
                    JOIN product_template_attribute_line ptal ON ptal.product_tmpl_id = pt.id
                    JOIN product_attribute att ON ptal.attribute_id = att.id
             
            """
        return from_str

    def _where(self):
        return """
                WHERE so.confirmation_date > '2023-01-01' 
        """

    def _group_by(self):
        group_by_str = """
                GROUP BY ol.id, p.id, ptal.attribute_id
             """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as
                (
                %s %s %s %s
            )""", (
                AsIs(self._table), AsIs(self._select()), AsIs(self._from()), AsIs(self._where()),
                AsIs(self._group_by()),))
