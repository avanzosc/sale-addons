# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizCatchAttachmentFromProduct(models.TransientModel):
    _name = "wiz.catch.attachment.from.product"
    _description = "Wizard for catch attachments from product"

    sale_order_line_id = fields.Many2one(
        string="Sale order line", comodel_name="sale.order.line"
    )
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="wiz.catch.attachment.from.product.line",
        inverse_name="wiz_id",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_line = self.env["sale.order.line"].browse(
            self.env.context.get("active_id")
        )
        line_ids = []

        product = sale_line.product_id

        cond_template = [
            ("attach_in_sales_orders", "=", True),
            ("res_model", "=", "product.template"),
            ("res_id", "in", product.product_tmpl_id.ids),
        ]
        attachments_template = self.env["ir.attachment"].search(cond_template)

        cond_product = [
            ("attach_in_sales_orders", "=", True),
            ("res_model", "=", "product.product"),
            ("res_id", "in", [product.id]),
        ]
        attachments_product = self.env["ir.attachment"].search(cond_product)
        attachments = attachments_template + attachments_product

        for attachment in attachments:
            cond_line = [
                ("res_model", "=", "sale.order.line"),
                ("res_id", "=", sale_line.id),
                ("name", "=", attachment.name),
            ]
            attachment2 = self.env["ir.attachment"].search(cond_line, limit=1)
            if not attachment2:
                line_ids += [
                    (
                        0,
                        0,
                        {
                            "attachment_id": attachment.id,
                            "attachment_name": attachment.name,
                        },
                    )
                ]
        res.update({"sale_order_line_id": sale_line.id, "line_ids": line_ids})
        return res

    def button_catch_attachment_from_product(self):
        for line in self.line_ids.filtered(lambda x: x.catch_attachment):
            product = self.sale_order_line_id.product_id
            attachments_to_copy = self.env["ir.attachment"]
            cond_template = [
                ("res_model", "=", "product.template"),
                ("res_id", "in", product.product_tmpl_id.ids),
                ("name", "=", line.attachment_name),
            ]
            attachments_to_copy += self.env["ir.attachment"].search(cond_template)
            cond_product = [
                ("res_model", "=", "product.product"),
                ("res_id", "in", [product.id]),
                ("name", "=", line.attachment_name),
            ]
            attachments_to_copy += self.env["ir.attachment"].search(cond_product)
            for attachment in attachments_to_copy:
                attachment.copy(
                    {
                        "res_model": "sale.order.line",
                        "res_id": self.sale_order_line_id.id,
                    }
                )


class WizCatchAttachmentFromProductLine(models.TransientModel):
    _name = "wiz.catch.attachment.from.product.line"
    _description = "Lines of wizard for catch attachments from product"

    wiz_id = fields.Many2one(
        string="Wizard", comodel_name="wiz.catch.attachment.from.product"
    )
    catch_attachment = fields.Boolean(string="Catch attachment", default=False)
    attachment_id = fields.Many2one(string="Attachment", comodel_name="ir.attachment")
    attachment_name = fields.Char(string="Attachment name")
