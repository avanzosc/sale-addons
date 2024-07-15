# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

import pytz

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.models import expression


class SaleOrderImportLine(models.Model):
    _name = "sale.order.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import sale orders"

    import_id = fields.Many2one(
        comodel_name="sale.order.import",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="import_id.company_id",
        store=True,
    )
    action = fields.Selection(
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    sale_order_id = fields.Many2one(string="sale Order", comodel_name="sale.order")
    client_order_ref = fields.Char(
        string="Customer Order Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_code = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_barcode = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_vat = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_reference = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_vat = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_reference = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_id = fields.Many2one(
        string="Invoice Address",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_name = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_vat = fields.Char(
        string="Delivery Address vat",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_reference = fields.Char(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date_order = fields.Date(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_date = fields.Date(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    quantity = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    price_unit = fields.Float(
        states={"done": [("readonly", True)]},
        copy=False,
    )
    total_order_amount = fields.Float(
        string="Total order amount",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        log_infos = []
        sale, log_info_origin = self._check_origin()
        if log_info_origin:
            log_infos.append(log_info_origin)
        product, log_info_product = self._check_product()
        if log_info_product:
            log_infos.append(log_info_product)
        customer = self.customer_id
        if not self.customer_id:
            partner = self._check_partner(
                self.customer_name,
                self.customer_reference,
                self.customer_vat,
            )
            if not partner:
                log_infos.append(_("Customer not found."))
            if len(partner) > 1:
                log_infos.append(_("More than one customer already exist."))
            customer = partner
        invoice_address = self.invoice_address_id
        if not self.invoice_address_id and (
            self.invoice_address_name
            or self.invoice_address_reference
            or self.invoice_address_vat
        ):
            partner = self._check_partner(
                self.invoice_address_name,
                self.invoice_address_reference,
                self.invoice_address_vat,
            )
            if not partner:
                log_infos.append(_("Invoice Address not found."))
            if len(partner) > 1:
                log_infos.append(_("More than one Invoice Address already exist."))
            invoice_address = partner
        delivery_address = self.delivery_address_id
        if not self.delivery_address_id and (
            self.delivery_address_name
            or self.delivery_address_reference
            or self.delivery_address_vat
        ):
            partner = self._check_partner(
                self.delivery_address_name,
                self.delivery_address_reference,
                self.delivery_address_vat,
            )
            if not partner:
                log_infos.append(_("Delivery Address not found."))
            if len(partner) > 1:
                log_infos.append(_("More than one Delivery Address already exist."))
            delivery_address = partner
        state = "error" if log_infos else "pass"
        action = "create"
        update_values.update(
            {
                "product_id": product and product.id,
                "customer_id": customer and customer.id,
                "invoice_address_id": invoice_address and invoice_address.id,
                "delivery_address_id": delivery_address and delivery_address.id,
                "log_info": "\n".join(log_infos),
                "state": state,
                "action": action,
            }
        )
        return update_values

    def _check_origin(self):
        log_info = ""
        error = _(
            "Error: Rows with the same Customer Order Reference have "
            "different information for importing sales order header "
            "data."
        )
        search_domain = [("client_order_ref", "=", self.client_order_ref)]
        sale = self.env["sale.order"].search(search_domain, limit=1)
        if sale:
            if not sale.sale_import_id or sale.sale_import_id != self.import_id:
                log_info = _(
                    "Error: Sale Order already exist with this Client Order "
                    "Ref.: %(client_order_ref)s."
                ) % {
                    "client_order_ref": self.client_order_ref,
                }
        if not log_info:
            lines = self.import_id.import_line_ids.filtered(
                lambda x: x.client_order_ref == self.client_order_ref
            )
            if lines:
                found = lines.filtered(
                    lambda x: x.customer_name != self.customer_name
                    or x.customer_vat != self.customer_vat
                    or x.customer_reference != self.customer_reference
                    or x.invoice_address_name != self.invoice_address_name
                    or x.invoice_address_vat != self.invoice_address_vat
                    or x.invoice_address_reference != self.invoice_address_reference
                    or x.delivery_address_name != self.delivery_address_name
                    or x.delivery_address_vat != self.delivery_address_vat
                    or x.delivery_address_reference != self.delivery_address_reference
                    or x.date_order != self.date_order
                    or x.delivery_date != self.delivery_date
                    or x.total_order_amount != self.total_order_amount
                )
                if found:
                    log_info = error
        return sale, log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        product_obj = self.env["product.product"]
        if self.product_name:
            search_domain = [("name", "=", self.product_name)]
        else:
            search_domain = []
        if self.product_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.product_code)], search_domain]
            )
        if self.product_barcode:
            search_domain = expression.AND(
                [[("barcode", "=", self.product_barcode)], search_domain]
            )
        search_domain = expression.AND(
            [
                [
                    "|",
                    ("company_id", "=", self.import_id.company_id.id),
                    ("company_id", "=", False),
                ],
                search_domain,
            ]
        )
        products = product_obj.search(search_domain)
        if len(products) > 1:
            products = False
            log_info = _("More than one product already exist.")
        if not products and "from_sale_wizard_laser" not in self.env.context:
            log_info = _("Product not found.")
        return products, log_info

    def _check_partner(self, name, reference, vat):
        self.ensure_one()
        partner_obj = self.env["res.partner"]
        if self.import_id.company_id:
            partner_obj = partner_obj.with_company(self.import_id.company_id)
        search_domain = [("name", "=", name)]
        if reference:
            search_domain = expression.OR([[("ref", "=", reference)], search_domain])
        if vat:
            search_domain = expression.OR([[("vat", "=", vat)], search_domain])
        if self.import_id.company_id:
            search_domain = expression.AND(
                [
                    [
                        "|",
                        ("company_id", "=", self.import_id.company_id.id),
                        ("company_id", "=", False),
                    ],
                    search_domain,
                ]
            )
        contacts = partner_obj.search(search_domain)
        return contacts

    def _action_process(self):
        update_values = super()._action_process()
        if self.import_id.company_id:
            self = self.with_company(self.import_id.company_id)
        if self.action == "create":
            sale_line = self._create_sale_line()
            state = "done"
            update_values.update(
                {
                    "sale_order_id": sale_line.order_id and sale_line.order_id.id,
                    "log_info": "",
                    "state": state,
                }
            )
        return update_values

    def _create_sale_line(self):
        self.ensure_one()
        if self.client_order_ref:
            sale, log_info_origin = self._check_origin()
            if log_info_origin:
                raise UserError(log_info_origin)
            if not sale:
                sale = self._create_sale_order()
        else:
            sale = self._create_sale_order()
        return self._create_sale_order_line(sale)

    def _create_sale_order(self):
        sale_obj = self.env["sale.order"]
        values = self._sale_order_values()
        new_sale = sale_obj.new(values)
        for comp_onchange in new_sale._onchange_methods["partner_id"]:
            comp_onchange(new_sale)
        vals = new_sale._convert_to_write(new_sale._cache)
        if self.invoice_address_id:
            vals["partner_invoice_id"] = self.invoice_address_id.id
        if self.delivery_address_id:
            vals["partner_shipping_id"] = self.delivery_address_id.id
        return sale_obj.create(vals)

    def _create_sale_order_line(self, sale):
        values = self._sale_order_line_values(sale)
        sale_line = self.env["sale.order.line"].create(values)
        return sale_line

    def _sale_order_values(self):
        values = {
            "partner_id": self.customer_id.id,
            "company_id": self.company_id.id,
            "sale_import_id": self.import_id.id,
        }
        if self.date_order:
            date_order = "{} 08:00:00".format(fields.Date.to_string(self.date_order))
            date_order = datetime.strptime(date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            date_order = timezone.localize(date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            values["date_order"] = date_order
        if self.delivery_date:
            delivery_date = "{} 08:00:00".format(
                fields.Date.to_string(self.delivery_date)
            )
            delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get("tz") or "UTC")
            delivery_date = timezone.localize(delivery_date).astimezone(pytz.UTC)
            delivery_date = delivery_date.replace(tzinfo=None)
            values["commitment_date"] = delivery_date
        if self.client_order_ref:
            values["client_order_ref"] = self.client_order_ref
        if self.total_order_amount:
            values["total_amount_from_import"] = self.total_order_amount
        return values

    def _sale_order_line_values(self, sale):
        values = {
            "order_id": sale.id,
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "product_uom": self.product_id.uom_id.id,
            "product_uom_qty": self.quantity,
            "price_unit": self.price_unit,
        }
        return values
