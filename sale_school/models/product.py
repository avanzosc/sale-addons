# Copyright 2019 Daniel Campos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

PRODUCT_TYPE = [
    ("canteen", "School Canteen"),
    ("home_meal", "Home Meal"),
    ("one_way", "One-way"),
    ("two_way", "Two-way"),
    ("death_insurance", "Parent Death Insurance"),
    ("first_contribution", "First Child Contribution"),
    ("second_contribution", "Second Child Contribution"),
]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    center_id = fields.Many2one(
        comodel_name='res.partner', string='Center',
        domain=[('educational_category', '=', 'school')])
    education_type = fields.Selection(
        selection=PRODUCT_TYPE, string="Product Type")
