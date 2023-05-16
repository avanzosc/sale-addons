# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons.base_import_wizard.models.base_import import convert2str
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ReturnableStockImport(models.Model):
    _name = "returnable.stock.import"
    _inherit = "base.import"
    _description = "Wizard to import returnable product stock"

    import_line_ids = fields.One2many(
        comodel_name="returnable.stock.import.line",
    )
    sale_count = fields.Integer(
        string="# Sales",
        compute="_compute_sale_count",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company.id
    )

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            sale_partner_ref = row_values.get("CodigoCliente", "")
            sale_partner_name = row_values.get("NombreCliente", "")
            sale_product_name = row_values.get("NombreProducto", "")
            sale_product_code = row_values.get("CodigoProducto", "")
            sale_qty = row_values.get("Cantidad", "")
            sale_price_unit = row_values.get("PrecioUnitario", "")
            sale_order_type = row_values.get("TipoDePedido", "")
            log_info = ""
            values.update(
                {
                    "sale_partner_ref": convert2str(sale_partner_ref),
                    "sale_partner_name": convert2str(sale_partner_name),
                    "sale_product_name": convert2str(sale_product_name),
                    "sale_product_code": convert2str(sale_product_code),
                    "sale_qty": sale_qty,
                    "sale_price_unit": sale_price_unit,
                    "sale_order_type": convert2str(sale_order_type),
                    "log_info": log_info,
                }
            )
        return values

    def _compute_sale_count(self):
        for record in self:
            record.sale_count = len(
                record.mapped("import_line_ids.sale_id"))

    def button_open_sale(self):
        self.ensure_one()
        sales = self.mapped("import_line_ids.sale_id")
        action = self.env.ref("sale.action_quotations_with_onboarding")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", sales.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict


class ReturnableStockImportLine(models.Model):
    _name = "returnable.stock.import.line"
    _inherit = "base.import.line"
    _description = "Wizard lines to import returnable product stock"

    import_id = fields.Many2one(
        comodel_name="returnable.stock.import",
    )
    action = fields.Selection(
        string="Action",
        selection_add=[
            ("create", "Create"),
        ],
        ondelete={"create": "set default"},
        states={"done": [("readonly", True)]},
    )
    sale_id = fields.Many2one(
        string="Sale",
        comodel_name="sale.order")
    sale_partner_ref = fields.Char(
        string="Partner Ref",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_partner_name = fields.Char(
        string="Partner Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_product_code = fields.Char(
        string="Product Code",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_product_name = fields.Char(
        string="Product Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_qty = fields.Float(
        string="Quantity",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_price_unit = fields.Float(
        string="Price Unit",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    sale_order_type = fields.Char(
        string="Order Type Name",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        states={"done": [("readonly", True)]},
        copy=False,
        )
    sale_order_type_id = fields.Many2one(
        string="Order Type",
        comodel_name="sale.order.type",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_validate(self):
        update_values = super()._action_validate()
        line_values = []
        for line in self.filtered(lambda l: l.state != "done"):
            log_info = ""
            partner = product = sale_type = False
            partner, log_info_partner = line._check_partner()
            if log_info_partner:
                log_info += log_info_partner
            product, log_info_product = line._check_product()
            if log_info_product:
                log_info += log_info_product
            sale_type, log_info_sale_type = line._check_sale_type()
            if log_info_sale_type:
                log_info += log_info_sale_type
            if line.sale_qty == 0:
                log_info += _("Error: Will not charge.")
            if line.sale_qty < 0 and line.sale_price_unit != 0:
                log_info += _("Error: Negative quantity with price.")
            if line.partner_id and line.product_id and line.sale_price_unit:
                same_lines = line.import_id.import_line_ids.filtered(
                    lambda c: c.partner_id == line.partner_id and (
                        c.product_id == line.product_id) and (
                            c.sale_price_unit == line.sale_price_unit) and (
                                c.id != line.id))
                if same_lines:
                    log_info += _("Error: Duplicate line.")
            state = "error" if log_info or not (
                product) or not partner or not sale_type else "pass"
            action = "nothing"
            if state != "error":
                action = "create"
            update_values = {
                "partner_id": partner and partner.id,
                "product_id": product and product.id,
                "sale_order_type_id": sale_type and sale_type.id,
                "log_info": log_info,
                "state": state,
                "action": action,
                    }
            line_values.append(
                (
                    1,
                    line.id,
                    update_values,
                )
            )
        return line_values

    def _action_process(self):
        update_values = super()._action_process()
        line_values = []
        sale = False
        for line in self.filtered(lambda l: l.state not in ("error", "done")):
            log_info = ""
            if not line.partner_id:
                log_info += _("Error: The partner is required.")
            if not line.product_id:
                log_info += _("Error: The product is required.")
            if not line.sale_order_type_id:
                log_info += _("Error: The order type is required.")
            same_order = line.import_id.import_line_ids.filtered(
                lambda c: c.partner_id == line.partner_id)
            if same_order.filtered(lambda c: c.state == "error" and c != line):
                log_info += _("Error: There is another line with the " +
                              "same supplier and sale type with errors.")
            if log_info:
                state = "error"
                action = "nothing"
                line.write({
                        "log_info": log_info,
                        "state": state,
                        "action": action})
            elif line.action == "create":
                sale = line._create_sale_order()
                line._create_sale_order_lines(sale, same_order)
                sale.action_confirm()
                sale = sale.id
            else:
                continue
            state = "error" if log_info else "done"
            line.write({
                "sale_id": sale,
                "log_info": log_info,
                "state": state})
            line_values.append(
                (
                    1,
                    line.id,
                    {
                        "sale_id": sale,
                        "log_info": log_info,
                        "state": state,
                    },
                )
            )
        return line_values

    def _check_partner(self):
        self.ensure_one()
        log_info = ""
        if self.partner_id:
            return self.partner_id, log_info
        partner_obj = self.env["res.partner"]
        search_domain = []
        if self.sale_partner_name:
            search_domain = expression.AND(
                [[("name", "=", self.sale_partner_name)], search_domain])
        elif self.sale_partner_ref:
            search_domain = expression.AND(
                [[("ref", "=", self.sale_partner_ref)], search_domain])
        partners = partner_obj.search(search_domain)
        if not partners:
            partners = False
            log_info = _("Error: No partner found.")
        elif len(partners) > 1:
            partners = False
            log_info = _(
                "Error: More than one partner.")
        return partners and partners[:1], log_info

    def _check_product(self):
        self.ensure_one()
        log_info = ""
        if self.product_id:
            return self.product_id, log_info
        search_domain = []
        if self.sale_product_code:
            search_domain = expression.AND(
                [[("default_code", "=", self.sale_product_code)],
                 search_domain])
        elif self.sale_product_name:
            search_domain = expression.AND(
                [[("name", "=", self.sale_product_name)], search_domain])
        product_obj = self.env["product.product"]
        products = product_obj.search(search_domain)
        if not products:
            products = False
            log_info = _("Error: No product found.")
        elif len(products) > 1:
            products = False
            log_info = _(
                "Error: More than one product found.")
        return products and products[:1], log_info

    def _check_sale_type(self):
        self.ensure_one()
        log_info = ""
        if self.sale_order_type_id:
            return self.sale_order_type_id, log_info
        sale_type_obj = self.env["sale.order.type"]
        search_domain = []
        if self.sale_order_type:
            search_domain = expression.AND([[
                ("name", "=", self.sale_order_type)], search_domain])
        sale_types = sale_type_obj.search(search_domain)
        if not sale_types:
            sale_types = False
            log_info = _("Error: No sale type found.")
        elif len(sale_types) > 1:
            sale_types = False
            log_info = _(
                "Error: More than one sale type found")
        return sale_types and sale_types[:1], log_info

    def _create_sale_order(self):
        self.ensure_one()
        sale = self.env["sale.order"].create({
            "partner_id": self.partner_id.id,
            "partner_invoice_id": self.partner_id.id,
            "partner_shipping_id": self.partner_id.id,
            "type_id": self.sale_order_type_id.id,
            "warehouse_id": self.sale_order_type_id.warehouse_id.id,
            "company_id": self.import_id.company_id.id})
        return sale

    def _create_sale_order_lines(self, sale=False, lines=False):
        self.ensure_one()
        if lines and sale:
            for line in lines:
                self.env["sale.order.line"].create({
                    "product_id": line.product_id.id,
                    "name": line.product_id.name,
                    "product_uom_qty": 0,
                    "pending_qty": line.sale_qty,
                    "product_uom": line.product_id.uom_id.id,
                    "price_unit": line.sale_price_unit,
                    "order_id": sale.id})
