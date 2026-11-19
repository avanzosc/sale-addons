# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_offer_type = fields.Boolean(
        string="Is it offer type?",
        default=False,
    )
    from_offer_id = fields.Many2one(
        string="From offer",
        comodel_name="sale.order",
        copy=False,
    )
    introduction = fields.Text()
    acceptance_date = fields.Date(
        copy=False,
    )
    rejection_date = fields.Date(
        copy=False,
    )
    stage = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("pending", "Pending"),
        ],
        string="Offer Status",
        default="pending",
    )
    sale_ids = fields.One2many(
        string="Sales Order",
        comodel_name="sale.order",
        inverse_name="from_offer_id",
    )
    count_sale_orders = fields.Integer(
        string="Sale Order Count",
        compute="_compute_count_sale_orders",
    )
    previous_offers_count = fields.Integer(
        string="# Previous Offers", compute="_compute_previous_offers_count"
    )

    @api.depends("sale_ids")
    def _compute_count_sale_orders(self):
        for sale in self.with_context(active_test=False):
            sale.count_sale_orders = len(sale.sale_ids)

    def _compute_previous_offers_count(self):
        for sale in self:
            if not sale.from_offer_id:
                sale.previous_offers_count = 0
                continue
            cond = [
                ("unrevisioned_name", "=", sale.from_offer_id.unrevisioned_name),
                ("id", "<", sale.from_offer_id.id),
            ]
            offers = self.env["sale.order"].search(cond)
            sale.previous_offers_count = len(offers)

    @api.model
    def _default_type_id(self):
        if "default_is_offer_type" in self.env.context and self.env.context.get(
            "default_is_offer_type", False
        ):
            cond = [("is_offer_type", "=", True)]
            return self.env["sale.order.type"].search(cond, limit=1)
        return super()._default_type_id()

    @api.onchange("type_id")
    def onchange_type_id(self):
        for order in self:
            order.is_offer_type = order.type_id and order.type_id.is_offer_type

    def action_confirm(self):
        if any(self.filtered("is_offer_type")):
            raise UserError(_("It is not allowed to confirm an offer type sale order"))
        return super().action_confirm()

    def action_offer_to_quotation(self):
        for offer in self.filtered(lambda x: x.is_offer_type):
            cond = [("is_offer_type", "=", False)]
            normal_type = self.env["sale.order.type"].search(cond, limit=1)
            default = {
                "type_id": normal_type.id,
                "is_offer_type": normal_type.is_offer_type,
                "from_offer_id": offer.id,
            }
            offer.copy(default)

    @api.onchange("stage")
    def onchange_stage(self):
        for order in self:
            vals = {
                "acceptance_date": False,
                "rejection_date": False,
            }
            if order.stage == "accepted":
                vals["acceptance_date"] = fields.Date.context_today(self)
            if order.stage == "rejected":
                vals["rejection_date"] = fields.Date.context_today(self)
            order.update(vals)

    def action_view_sale_orders(self):
        self.ensure_one()
        action = self.env.ref("sale.action_quotations")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [
                    (
                        "id",
                        "in",
                        self.with_context(active_test=False).mapped("sale_ids").ids,
                    )
                ],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update(
            {
                "domain": domain,
            }
        )
        return action_dict

    def action_view_previous_offers(self):
        self.ensure_one()
        cond = [
            ("unrevisioned_name", "=", self.from_offer_id.unrevisioned_name),
            ("id", "<", self.from_offer_id.id),
        ]
        offers = self.env["sale.order"].search(cond)
        action = self.env.ref("sale_order_offer_version.action_sale_offer")
        action_dict = action and action.read()[0]
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        domain = expression.AND(
            [
                [("id", "in", offers.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def _prepare_revision_data(self, new_revision):
        vals = super()._prepare_revision_data(new_revision)
        vals["active"] = True
        allow_modification_old_offers = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_order_offer_version.allow_modification_old_offers")
        )
        if allow_modification_old_offers:
            del vals["state"]
        return vals

    def _get_new_rev_data(self, new_rev_number):
        self.ensure_one()
        vals = super()._get_new_rev_data(new_rev_number)
        if "name" in vals and "-00-" in vals["name"]:
            vals["name"] = vals["name"].replace("-00-", "-")
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New") and vals.get("type_id"):
                sale_type = self.env["sale.order.type"].browse(vals["type_id"])
                if sale_type.sequence_id:
                    name = sale_type.sequence_id.next_by_id(
                        sequence_date=vals.get("date_order")
                    )
                    vals["name"] = name
                    if "is_offer_type" in vals and vals.get("is_offer_type", False):
                        vals["name"] = f"{name}-00"
        return super().create(vals_list)
