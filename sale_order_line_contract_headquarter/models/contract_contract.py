# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")

    def _prepare_invoice(self, date_invoice, journal=None):
        invoice_vals, move_form = super(
            ContractContract, self)._prepare_invoice(
                date_invoice, journal=journal)
        if self.headquarter_id:
            invoice_vals['headquarter_id'] = self.headquarter_id.id
        return invoice_vals, move_form
