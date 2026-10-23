# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ExportEducationRecordReport(models.TransientModel):
    _name = "report.catalog.product_xlsx.export"
    _description = "Wizard to export catalog records in xlsx"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    catalog_id = fields.Many2one(
        string="Catalog",
        comodel_name="product.catalog",
    )

    # @api.multi
    def export_xls(self):
        report_action = self.env.ref(
            "sale_product_catalog.catalog_product_record_xlsx"
        ).report_action(
            None,
            data={
                "partner_id": self.partner_id.id,
                "catalog_id": self.catalog_id.id,
            },
        )
        return report_action
