from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    producer = fields.Many2one(
        comodel_name="res.partner",
    )
    product_link = fields.Char(
        related="producer.website",
        string="Product Link",
        readonly=False,
    )

    @api.onchange("product_id")
    def _onchange_product_id_producer(self):
        if self.product_id:
            seller = self.product_id.product_tmpl_id.seller_ids.sorted("sequence")[:1]
            self.producer = seller.partner_id if seller else False
        else:
            self.producer = False
