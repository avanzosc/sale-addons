# Copyright 2024 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging
import os

from odoo import fields, models

_logger = logging.getLogger(__name__)

try:
    import ftplib
except ImportError as err:  # pragma: no cover
    _logger.debug(err)


class ProductCatalogFtp(models.Model):
    _name = "product.catalog.ftp"
    _description = "Upload Catalog to FTP"

    active = fields.Boolean(default=True)
    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        string="Product Catalog",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        ondelete="cascade",
    )
    ftp_server = fields.Char(string="FTP Host")
    ftp_user = fields.Char(string="FTP Login", help="Login to connect to ftp server")
    ftp_password = fields.Char(string="FTP Password")
    ftp_timeout = fields.Integer(
        string="FTP Timeout",
        default=30,
    )
    ftp_folder = fields.Char(
        string="FTP Folder",
        default="/",
        help="Folder name in FTP server",
    )
    ftp_error = fields.Text(
        readonly=True,
    )

    _sql_constraints = [
        (
            "catalog_partner_uniq",
            "unique (catalog_id,partner_id)",
            "Catalogs can only be uploaded once per partner !",
        )
    ]

    def _get_local_folder(self):
        self.ensure_one()

        params = self.env["ir.config_parameter"].sudo()
        folder_name = params.get_param(
            "product_catalog_ftp.base_ftp_folder", default="ftp_catalog"
        )

        local_folder = os.path.join(
            os.path.expanduser("~/"),
            folder_name,
            str(self.partner_id.id),
            str(self.catalog_id.id),
        )

        if not os.path.exists(local_folder):
            os.makedirs(local_folder)
        return local_folder

    def _get_datas_fname(self):
        self.ensure_one()
        return "catalog_{}.xlsx".format(self.catalog_id.name.replace(" ", "_"))

    def _connect_ftp(self):
        self.ensure_one()
        return ftplib.FTP(
            host=self.ftp_server,
            user=self.ftp_user,
            passwd=self.ftp_password,
            timeout=self.ftp_timeout,
        )

    def empty_local_folder(self):
        local_folder = self._get_local_folder()
        for file in os.listdir(local_folder):
            file_path = os.path.join(local_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def upload_file(self, filename):
        self.ensure_one()
        ftp_error = ""
        datas_fname = self._get_datas_fname()
        try:
            ftp_server = self._connect_ftp()

            # Read file in binary mode
            with open(filename, "rb") as file:
                # Command for Uploading the file "STOR filename"
                server_filename = os.path.join(self.ftp_folder or "/", datas_fname)
                ftp_server.storbinary(f"STOR {server_filename}", file)

            ftp_server.quit()
        except Exception as e:
            ftp_error = e
        self.write(
            {
                "ftp_error": ftp_error,
            }
        )
        return True

    def remove_ftp_file(self):
        self.ensure_one()
        ftp_error = ""
        datas_fname = self._get_datas_fname()
        server_filename = os.path.join(self.ftp_folder or "/", datas_fname)
        try:
            ftp_server = self._connect_ftp()
            ftp_server.delete(server_filename)
            ftp_server.quit()
        except Exception as e:
            ftp_error = e
        self.write(
            {
                "ftp_error": ftp_error,
            }
        )
        return True

    def create_catalog(self):
        self.ensure_one()

        local_folder = self._get_local_folder()
        self.empty_local_folder()

        datas_fname = self._get_datas_fname()
        filename = os.path.join(local_folder, datas_fname)

        render_data = {
            "partner_id": self.partner_id.id,
            "catalog_id": self.catalog_id.id,
        }
        data, data_format = self.env["ir.actions.report"]._render(
            "sale_product_catalog.catalog_product_record_xlsx",
            self.catalog_id.ids,
            data=render_data,
        )

        xlsx_file = open(filename, "wb")
        xlsx_file.write(data)
        xlsx_file.close()

        if self.ftp_server and self.ftp_user and self.ftp_password:
            self.upload_file(filename)
        return True

    def write(self, values):
        if (
            "active" in values
            and not values["active"]
            or "partner_id" in values
            or "catalog_id" in values
        ):
            for record in self:
                record.empty_local_folder()
                record.remove_ftp_file()
        return super().write(values)

    def unlink(self):
        for record in self:
            record.empty_local_folder()
            record.remove_ftp_file()
        return super().unlink()

    def _create_catalog_file_cron(self):
        upload_catalogs = self.search([])
        for upload_catalog in upload_catalogs:
            upload_catalog.create_catalog()
