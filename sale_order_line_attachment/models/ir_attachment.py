# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    attach_in_sales_orders = fields.Boolean(
        string='Attach in sales orders', default=True)
    
    show_attach_in_sale = fields.Boolean(
        string= 'Is product attachment',
        compute = '_compute_show_attach_in_sale',
    )

    @api.depends('res_model')
    def _compute_show_attach_in_sale(self):
        for att in self:
            att.show_attach_in_sale = (att.res_model == 'product.template')
