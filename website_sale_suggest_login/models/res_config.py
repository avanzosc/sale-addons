# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    website_checkout_redirect = fields.Selection(
        selection=[('login', 'Login'),
                   ('create_account', 'Create Account')],
        string='Website Checkout Redirect', default='login')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_checkout_redirect = fields.Selection(
        'Website Checkout Redirect',
        related='company_id.website_checkout_redirect', readonly=False)
