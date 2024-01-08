# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.addons.base_import_wizard.models.base_import import (convert2date,
                                                               convert2str)
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval

str2date = fields.Date.to_date


class SaleOrderImport(models.Model):
    _name = "sale.order.import"
    _inherit = "base.import"
    _description = "Wizard to import sale orders"

    import_line_ids = fields.One2many(
        comodel_name="sale.order.import.line",
    )
    sale_order_count = fields.Integer(
        string="# Sale Orders",
        compute="_compute_sale_order_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id,
    )
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name="stock.warehouse")

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            date_order = row_values.get("FechaPedido", "")
            delivery_date = row_values.get("FechaEntrega", "")
            client_order_ref = row_values.get("NumeroPedidoCliente", "")
            product_name = row_values.get("NombreProducto", "")
            product_code = row_values.get("CodigoProducto", "")
            product_barcode = row_values.get("CodigoBarrasProducto", "")
            customer_name = row_values.get("NombreCliente", "")
            customer_code = row_values.get("CodigoCliente", "")
            customer_reference = row_values.get("ReferenciaCliente", "")
            product_customer_code = row_values.get("CodigoProductoCliente", "")
            invoice_address_name = row_values.get("NombreDireccionFacturacion", "")
            invoice_address_code = row_values.get("CodigoDireccionFacturacion", "")
            invoice_address_reference = row_values.get(
                "ReferenciaDireccionFacturacion", ""
            )
            delivery_address_name = row_values.get("NombreDireccionEnvio", "")
            delivery_address_code = row_values.get("CodigoDireccionEnvio", "")
            delivery_address_reference = row_values.get("ReferenciaDireccionEnvio", "")
            values.update(
                {
                    "client_order_ref": convert2str(client_order_ref),
                    "product_name": convert2str(product_name),
                    "product_code": convert2str(product_code),
                    "product_barcode": convert2str(product_barcode),
                    "customer_name": convert2str(customer_name),
                    "customer_code": convert2str(customer_code),
                    "customer_reference": convert2str(customer_reference),
                    "product_customer_code": convert2str(product_customer_code),
                    "invoice_address_name": convert2str(invoice_address_name),
                    "invoice_address_code": convert2str(invoice_address_code),
                    "invoice_address_reference": convert2str(invoice_address_reference),
                    "delivery_address_name": convert2str(delivery_address_name),
                    "delivery_address_code": convert2str(delivery_address_code),
                    "delivery_address_reference": convert2str(
                        delivery_address_reference
                    ),
                    "date_order": convert2date(date_order) if date_order else False,
                    "delivery_date": convert2date(delivery_date)
                    if delivery_date
                    else False,
                    "quantity": row_values.get("Cantidad", ""),
                    "price_unit": row_values.get("PrecioUnitario", ""),
                    "total_order_amount": row_values.get("TotalImportePedido", ""),
                    "log_info": "",
                }
            )
        return values

    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(
                record.mapped("import_line_ids.sale_order_id")
            )

    def button_open_sale_order(self):
        self.ensure_one()
        orders = self.mapped("import_line_ids.sale_order_id")
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        action["domain"] = expression.AND(
            [[("id", "in", orders.ids)], safe_eval(action.get("domain") or "[]")]
        )
        return action
