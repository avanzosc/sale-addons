# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
import unicodedata
from datetime import datetime
import pytz


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
        string="Action",
        selection=[
            ("create", "Create"),
            ("nothing", "Nothing"),
        ],
        default="nothing",
        states={"done": [("readonly", True)]},
        copy=False,
        required=True,
    )
    sale_order_id = fields.Many2one(
        string="sale Order",
        comodel_name="sale.order")
    client_order_ref = fields.Char(
        string="Customer Order Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_barcode = fields.Char(
        string="Product Barcode",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_name = fields.Char(
        string="Customer Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_code = fields.Char(
        string="Customer Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    customer_reference = fields.Char(
        string="Customer Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_customer_code = fields.Char(
        string="Product Customer Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_name = fields.Char(
        string="Invoice Address Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_code = fields.Char(
        string="Invoice Address Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    invoice_address_reference = fields.Char(
        string="Invoice Address Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_name = fields.Char(
        string="Delivery Address Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_code = fields.Char(
        string="Delivery Address Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_address_reference = fields.Char(
        string="Delivery Address Reference",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    date_order = fields.Date(
        string="Date Order",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    delivery_date = fields.Date(
        string="Delivery Date",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    quantity = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    price_unit = fields.Float(
        string="Price Unit",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    total_order_amount = fields.Float(
        string="Total order amount",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_customer_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_invoice_address_id = fields.Many2one(
        string="Invoice Address",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_delivery_address_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    description = fields.Text(
        string="Description",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    line_comment = fields.Text(
        string="Line Commend",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def action_validate(self):
        super().action_validate()
        line_values = []
        for line in self.filtered(lambda x: x.state != "done"):
            data = line.initialize_sale_data()
            if line.client_order_ref:
                data = line._check_origin(data)
            if not data.get("log_info"):
                if (line.invoice_address_name or line.invoice_address_code or
                    line.invoice_address_reference or
                    line.delivery_address_name or line.delivery_address_code or
                        line.delivery_address_reference):
                    data = line._check_invoice_delivery_address(data)
                if (line.customer_name or line.customer_code or
                        line.customer_reference):
                    data = line._check_customer(data)
                if (line.product_name or line.product_code or
                        line.product_barcode):
                    data = line._check_product(data)
                if line.product_customer_code:
                    data = line._check_product_customer_code(data)
            state = "error" if data.get("log_info") else "pass"
            action = "nothing"
            if state != "error":
                action = "create"
            update_values = line._get_update_values(data, state, action)
            line_values.append((1, line.id, update_values,))
        return line_values

    def initialize_sale_data(self):
        data = {
            "sale_product": False,
            "sale_customer": False,
            "sale_invoice_address": False,
            "sale_delivery_address": False,
            "log_info": False}
        return data

    def _check_origin(self, data):
        log_info = False
        error = _("Error: Rows with the same Customer Order Reference have "
                  "different information for importing sales order header "
                  "data.")
        search_domain = [("client_order_ref", "=", self.client_order_ref)]
        sales = self.env["sale.order"].search(search_domain, limit=1)
        if sales:
            log_info = _("Error: Previously uploaded order.")
        if not log_info:
            lines = self.import_id.import_line_ids.filtered(
                lambda x: x.client_order_ref == self.client_order_ref)
            if lines:
                found = lines.filtered(
                    lambda x: x.customer_name != self.customer_name or
                    x.customer_code != self.customer_code or
                    x.customer_reference != self.customer_reference or
                    x.invoice_address_name != self.invoice_address_name or
                    x.invoice_address_code != self.invoice_address_code or
                    x.invoice_address_reference !=
                    self.invoice_address_reference or
                    x.delivery_address_name != self.delivery_address_name or
                    x.delivery_address_code != self.delivery_address_code or
                    x.delivery_address_reference !=
                    self.delivery_address_reference or
                    x.date_order != self.date_order or
                    x.delivery_date != self.delivery_date or
                    x.total_order_amount != self.total_order_amount)
                if found:
                    log_info = error
        data["log_info"] = log_info
        return data

    def _check_invoice_delivery_address(self, data):
        if (self.invoice_address_name or self.invoice_address_code or
                self.invoice_address_reference):
            data = self._search_invoice_address(data)
        if (self.delivery_address_name or self.delivery_address_code or
                self.delivery_address_reference):
            data = self._search_delivery_address(data)
        partner_invoice_address = False
        partner_delivery_address = False
        if data.get("sale_invoice_address", False):
            invoice_address = data.get("sale_invoice_address")
            partner_invoice_address = (
                invoice_address if not invoice_address.parent_id else
                invoice_address.parent_id)
        if data.get("sale_delivery_address", False):
            delivery_address = data.get("sale_delivery_address")
            partner_delivery_address = (
                delivery_address if not delivery_address.parent_id else
                delivery_address.parent_id)
        log_info = data.get("log_info")
        if (partner_invoice_address and partner_delivery_address and
                partner_invoice_address != partner_delivery_address):
            error = _("Error: Different customers between delivery and billing"
                      " addresses.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if partner_invoice_address:
            data["sale_customer"] = partner_invoice_address
        if partner_delivery_address:
            data["sale_customer"] = partner_delivery_address
        data["log_info"] = log_info
        return data

    def _search_invoice_address(self, data):
        log_info = data.get("log_info")
        data, customer = self._search_customer(
            data, self.invoice_address_reference, self.invoice_address_name,
            self.invoice_address_code)
        if not customer:
            error = _("Error: Invoice Address not found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) > 1:
            error = _("Error: More than one Invoice Address found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) == 1:
            data["sale_invoice_address"] = customer
        data["log_info"] = log_info
        return data

    def _search_delivery_address(self, data):
        log_info = data.get("log_info")
        data, customer = self._search_customer(
            data, self.delivery_address_reference, self.delivery_address_name,
            self.delivery_address_code)
        if not customer:
            error = _("Error: Delivery Address not found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) > 1:
            error = _("Error: More than one Delivery Address found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) == 1:
            data["sale_delivery_address"] = customer
        data["log_info"] = log_info
        return data

    def _check_customer(self, data):
        log_info = data.get("log_info")
        if self.sale_customer_id:
            data["sale_customer"] = self.sale_customer_id
            return data
        data, customer = self._search_customer(
            data, self.customer_reference, self.customer_name,
            self.customer_code)
        if not customer:
            error = _("Error: Customer not found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) > 1:
            error = _("Error: More than one Customer found.")
            log_info = (
                error if not log_info else "{} {}".format(log_info, error))
        if customer and len(customer) == 1:
            if not data.get("sale_customer"):
                data["sale_customer"] = customer
            else:
                if data.get("sale_customer") != customer:
                    error = _(
                        "Error: Different customers found between "
                        "shipping/invoice addresses, and customer data "
                        "entered.")
                    log_info = (
                        error if not log_info else "{} {}".format(
                            log_info, error))
        data["log_info"] = log_info
        return data

    def _search_customer(self, data, address_reference, address_name,
                         address_code):
        customer_obj = self.env["res.partner"]
        search_domain = []
        customer = False
        if address_reference and not address_name:
            if not address_code:
                search_domain = [("ref", "=", address_reference)]
            else:
                search_domain = ["|", ("ref", "=", address_reference),
                                 ("customer_code", "=", address_code)]
        elif address_name and not address_reference:
            literal = "%{}".format(address_name)
            if not address_code:
                search_domain = ["|", ("name", "=ilike", address_name),
                                 ("name", "=ilike", literal)]
            else:
                search_domain = ["|", ("name", "=ilike", address_name),
                                 "|", ("name", "=ilike", literal),
                                 ("customer_code", "=", address_code)]
        elif address_reference and address_name:
            literal = "%{}%".format(address_name)
            if not address_code:
                search_domain = ["|", ("name", "=ilike", address_name),
                                 "|", ("name", "=ilike", literal),
                                 ("ref", "=", address_reference)]
            else:
                search_domain = ["|", ("name", "=ilike", address_name),
                                 "|", ("name", "=ilike", literal),
                                 "|", ("ref", "=", address_reference),
                                 ("customer_code", "=", address_code)]
        elif not address_reference and not address_name:
            if address_code:
                search_domain = [("customer_code", "=", address_code)]
        if search_domain:
            customer = customer_obj.search(search_domain)
            if customer and len(customer) > 1:
                search_domain = []
                if address_name:
                    literal = "%{}%".format(address_name)
                    search_domain = [
                        "|", ("name", "=ilike", address_name),
                        ("name", "=ilike", literal)
                    ]
                if address_reference:
                    search_domain.append(
                        ("ref", "=", address_reference))
                if address_code:
                    search_domain.append(
                        ("customer_code", "=", address_code))
                customer = customer_obj.search(search_domain)
        return data, customer

    def _check_product(self, data):
        if self.sale_product_id:
            data["sale_product"] = self.sale_product_id
            return data
        log_info = data.get("log_info")
        product_obj = self.env["product.product"]
        search_domain = []
        products = False
        if self.product_name:
            name = self.product_name.replace(" ", "")
            name = (
                ''.join((c for c in unicodedata.normalize(
                    'NFD', name) if unicodedata.category(c) != 'Mn')))
        if self.product_code and not self.product_name:
            if not self.product_barcode:
                search_domain = [("default_code", "=", self.product_code)]
            else:
                search_domain = ["|", ("default_code", "=", self.product_code),
                                 ("barcode", "=", self.product_barcode)]
        elif self.product_name and not self.product_code:
            if not self.product_barcode:
                search_domain = [("name", "=ilike", name)]
            else:
                search_domain = ["|", ("name", "=ilike", name),
                                 ("barcode", "=", self.product_barcode)]
        elif self.product_code and self.product_name:
            if not self.product_barcode:
                search_domain = ["|", ("name", "=ilike", name),
                                 ("default_code", "=", self.product_code)]
            else:
                search_domain = ["|", ("name", "=ilike", name),
                                 "|", ("default_code", "=", self.product_code),
                                 ("barcode", "=", self.product_barcode)]
        elif not self.product_code and not self.product_name:
            search_domain = [("barcode", "=", self.product_barcode)]
        if search_domain:
            products = product_obj.search(search_domain)
            if not products:
                error = _("Error: No product found.")
                log_info = (
                    error if not log_info else "{} {}".format(log_info, error))
            elif len(products) > 1:
                search_domain = []
                if self.product_name:
                    search_domain.append(
                        ("name", "=ilike", name))
                if self.product_code:
                    search_domain.append(
                        ("default_code", "=", self.product_code))
                if self.product_barcode:
                    search_domain.append(
                        ("barcode", "=", self.product_barcode))
                products = product_obj.search(search_domain)
                if len(products) == 0:
                    error = _("Error: No product found.")
                    log_info = (
                        error if not log_info else "{} {}".format(
                            log_info, error))
                if len(products) > 1:
                    error = _(
                        "Error: More than one product with the same name, or "
                        "code, or barcode found.")
                    log_info = (
                        error if not log_info else "{} {}".format(
                            log_info, error))
        if products and len(products) == 1:
            data["sale_product"] = products
        data["log_info"] = log_info
        return data

    def _check_product_customer_code(self, data):
        log_info = data.get("log_info")
        if data.get("sale_product") and self.product_customer_code:
            lines = data.get("sale_product").customer_ids.filtered(
                lambda x: x.product_code and
                x.product_code == self.product_customer_code)
            if not lines:
                error = _(
                    "Error: Product with Product Customer Code not found.")
                log_info = (
                    error if not log_info else "{} {}".format(log_info, error))
        if not data.get("sale_product") and self.product_customer_code:
            cond = [("product_code", "=", self.product_customer_code)]
            lines = self.env["product.customerinfo"].search(cond)
            if not lines:
                error = _(
                    "Error: Product with Product Customer Code not found.")
                log_info = (
                    error if not log_info else "{} {}".format(log_info, error))
            if len(lines) > 1:
                error = _(
                    "Error: More than one Product found with Product Customer "
                    "Code.")
                log_info = (
                    error if not log_info else "{} {}".format(log_info, error))
            if len(lines) == 1:
                if lines.product_id:
                    data["sale_product"] = lines.product_id
                    if (data.get("sale_customer") and lines.name and
                            data.get("sale_customer") != lines.name):
                        error = _(
                            "Error: Different client found with client data "
                            "entered, and client product code client.")
                        log_info = (
                            error if not log_info else "{} {}".format(
                                log_info, error))
                if (not lines.product_id and lines.product_tmpl_id and
                        lines.product_tmpl_id.product_variant_count == 1):
                    data["sale_product"] = (
                        lines.product_tmpl_id.product_variant_ids[0])
                    if (data.get("sale_customer") and lines.name and
                            data.get("sale_customer") != lines.name):
                        error = _(
                            "Error: Different client found with client data "
                            "entered, and client product code client.")
                        log_info = (
                            error if not log_info else "{} {}".format(
                                log_info, error))
                if (not lines.product_id and lines.product_tmpl_id and
                        lines.product_tmpl_id.product_variant_count > 1):
                    error = _(
                        "Error: More than one Product found with Product "
                        "Customer Code.")
                    log_info = (error if not log_info else "{} {}".format(
                        log_info, error))
        data["log_info"] = log_info
        return data

    def _get_update_values(self, data, state, action):
        sale_product = data.get("sale_product")
        sale_customer = data.get("sale_customer")
        sale_invoice_address = data.get("sale_invoice_address")
        sale_delivery_address = data.get("sale_delivery_address")
        update_values = {
            "sale_product_id": sale_product.id if sale_product else False,
            "sale_customer_id": sale_customer.id if sale_customer else False,
            "sale_invoice_address_id": (
                sale_invoice_address.id if sale_invoice_address else False),
            "sale_delivery_address_id": (
                sale_delivery_address.id if sale_delivery_address else False),
            "log_info": data.get("log_info"),
            "state": state,
            "action": action,
            }
        return update_values

    def action_process(self):
        super().action_validate()
        line_values = []
        origins = []
        for line in self.filtered(lambda x: x.state not in ("error", "done")):
            log_info = ""
            if line.action == "create":
                sale = False
                if not line.client_order_ref:
                    sale = line._create_sale_order()
                    line._create_sale_order_line(sale)
                if (line.client_order_ref and
                        (line.client_order_ref) not in (origins)):
                    if self.filtered(lambda z: z.client_order_ref == (
                            line.client_order_ref) and (z.state == "error")):
                        log_info = _(
                            "Error: There is another line with the same" +
                            " origin document with some errors.")
                    else:
                        data = line._check_origin({})
                        log_info = data.get("log_info")
                        if not log_info:
                            origins.append(line.client_order_ref)
                            sale = line._create_sale_order()
                            same_origin = self.filtered(
                                lambda y: y.client_order_ref == (
                                    line.client_order_ref))
                            for record in same_origin:
                                record._create_sale_order_line(sale)
            else:
                continue
            state = "error" if log_info else "done"
            vals = {"log_info": log_info,
                    "state": state}
            if sale:
                vals["sale_order_id"] = sale.id
            line.write(vals)
            line_values.append((1, line.id, vals))
        return line_values

    def _create_sale_order(self):
        sale_obj = self.env["sale.order"]
        values = self._sale_order_values()
        new_sale = sale_obj.new(values)
        for (comp_onchange) in (new_sale._onchange_methods["partner_id"]):
            comp_onchange(new_sale)
        vals = new_sale._convert_to_write(new_sale._cache)
        if self.sale_invoice_address_id:
            vals["partner_invoice_id"] = self.sale_invoice_address_id.id
        if self.sale_delivery_address_id:
            vals["partner_shipping_id"] = self.sale_delivery_address_id.id
        return sale_obj.create(vals)

    def _sale_order_values(self):
        values = {"partner_id": self.sale_customer_id.id,
                  "company_id": self.company_id.id,
                  "sale_import_id": self.import_id.id,
                  "note": self.description}
        if self.date_order:
            date_order = "{} 08:00:00".format(
                fields.Date.to_string(self.date_order))
            date_order = datetime.strptime(
                date_order, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get('tz') or 'UTC')
            date_order = timezone.localize(
                date_order).astimezone(pytz.UTC)
            date_order = date_order.replace(tzinfo=None)
            values["date_order"] = date_order
        if self.delivery_date:
            delivery_date = "{} 08:00:00".format(
                fields.Date.to_string(self.delivery_date))
            delivery_date = datetime.strptime(
                delivery_date, "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone(self._context.get('tz') or 'UTC')
            delivery_date = timezone.localize(
                delivery_date).astimezone(pytz.UTC)
            delivery_date = delivery_date.replace(tzinfo=None)
            values["commitment_date"] = delivery_date
        if self.client_order_ref:
            values["client_order_ref"] = self.client_order_ref
        if self.total_order_amount:
            values["total_amount_from_import"] = self.total_order_amount
        return values

    def _create_sale_order_line(self, sale):
        values = self._sale_order_line_values()
        sale.order_line = [(0, 0, values)]
        for line in sale.order_line:
            price_unit = line.price_unit
            line.product_id_change()
            line.product_uom_change()
            if price_unit:
                line.price_unit = price_unit

    def _sale_order_line_values(self):
        values = {
            "order_id": self.sale_order_id.id,
            "name": self.sale_product_id.name,
            "product_id": self.sale_product_id.id,
            "product_uom": self.sale_product_id.uom_id.id,
            "product_uom_qty": self.quantity,
            "price_unit": self.price_unit,
            "line_comment": self.line_comment}
        return values
