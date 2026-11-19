# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ExportEducationRecordReport(models.TransientModel):
    _name = "report.catalog.product_xlsx.export"
    _description = "Wizard to export catalog records in xlsx"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    catalog_id = fields.Many2one(
        string="Catalog",
        comodel_name="product.catalog.web",
    )

    def export_xls(self):
        report_name = "catalog.product_xlsx"
        print_report_name = _("Catalog Record")
        self.catalog_id = self.env.context.get("active_id")
        report = {
            "type": "ir.actions.report",
            "report_type": "xlsx",
            "report_name": report_name,
            "print_report_name": print_report_name,
            "context": dict(self.env.context, report_file="group_records"),
            "data": {
                "partner_id": self.partner_id.id,
                "catalog_id": self.catalog_id.id,
            },
        }
        return report
