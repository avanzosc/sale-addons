# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    requisition_id = fields.Many2one(
        comodel_name="sale.requisition",
        string="Sale Agreement",
        copy=False,
    )
    is_quantity_copy = fields.Selection(
        related="requisition_id.is_quantity_copy",
        readonly=False)

    @api.onchange("requisition_id")
    def _onchange_requisition_id(self):
        if not self.requisition_id:
            return

        requisition = self.requisition_id
        if self.partner_id:
            partner = self.partner_id
        else:
            partner = requisition.vendor_id
        payment_term = partner.property_payment_term_id

        FiscalPosition = self.env["account.fiscal.position"]
        fpos = FiscalPosition.with_context(
            force_company=self.company_id.id).get_fiscal_position(partner.id)
        fpos = FiscalPosition.browse(fpos)

        self.partner_id = partner.id
        self.fiscal_position_id = fpos.id
        self.payment_term_id = payment_term.id,
        self.company_id = requisition.company_id.id
        self.currency_id = requisition.currency_id.id
        if not self.origin or requisition.name not in self.origin.split(", "):
            if self.origin:
                if requisition.name:
                    self.origin = self.origin + ", " + requisition.name
            else:
                self.origin = requisition.name
        self.notes = requisition.description
        self.date_order = fields.Datetime.now()

        if requisition.type_id.line_copy != "copy":
            return

        # Create PO lines if necessary
        order_lines = []
        for line in requisition.line_ids:
            # Compute name
            product_lang = line.product_id.with_context(
                lang=partner.lang,
                partner_id=partner.id
            )
            name = product_lang.display_name
            if product_lang.description_sale:
                name += "\n" + product_lang.description_sale

            # Compute taxes
            if fpos:
                taxes_ids = fpos.map_tax(line.product_id.taxes_id.filtered(
                    lambda tax: tax.company_id == requisition.company_id)).ids
            else:
                taxes_ids = line.product_id.taxes_id.filtered(
                    lambda tax: tax.company_id == requisition.company_id).ids

            # Compute quantity and price_unit
            if line.product_uom_id != line.product_id.uom_id:
                product_qty = line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
                price_unit = line.product_uom_id._compute_price(
                    line.price_unit, line.product_id.uom_id)
            else:
                product_qty = line.product_qty
                price_unit = line.price_unit

            if requisition.type_id.quantity_copy != "copy":
                product_qty = 0

            # Create PO line
            order_line_values = line._prepare_sale_order_line(
                name=name, product_qty=product_qty, price_unit=price_unit,
                taxes_ids=taxes_ids)
            order_lines.append((0, 0, order_line_values))
        self.order_line = order_lines

    def button_confirm(self):
        res = super(SaleOrder, self).button_confirm()
        for so in self:
            if not so.requisition_id:
                continue
            if so.requisition_id.type_id.exclusive == "exclusive":
                others_so = so.requisition_id.mapped("purchase_ids").filtered(
                    lambda r: r.id != so.id)
                others_so.button_cancel()
                if so.state not in ["draft", "sent", "to approve"]:
                    so.requisition_id.action_done()
        return res

    @api.model
    def create(self, vals):
        sale = super(SaleOrder, self).create(vals)
        if sale.requisition_id:
            sale.message_post_with_view(
                "mail.message_origin_link",
                values={"self": sale, "origin": sale.requisition_id},
                subtype_id=self.env["ir.model.data"].xmlid_to_res_id("mail.mt_note"))
        return sale

    def write(self, vals):
        result = super(SaleOrder, self).write(vals)
        if vals.get("requisition_id"):
            self.message_post_with_view(
                "mail.message_origin_link",
                values={"self": self, "origin": self.requisition_id, "edit": True},
                subtype_id=self.env["ir.model.data"].xmlid_to_res_id("mail.mt_note"))
        return result


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_uom_qty", "product_uom")
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        if self.order_id.requisition_id:
            for line in self.order_id.requisition_id.line_ids.filtered(
                    lambda l: l.product_id == self.product_id):
                if line.product_uom_id != self.product_uom:
                    self.price_unit = line.product_uom_id._compute_price(
                        line.price_unit, self.product_uom)
                else:
                    self.price_unit = line.price_unit
                break
        return res
