from odoo import fields, http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        response = super().cart(access_token=access_token, revive=revive, **post)
        order = request.website.sale_get_order()

        if order and order.state != "draft":
            request.session["sale_order_id"] = None
            order = request.website.sale_get_order()

        if not order:
            last_order = request.env["sale.order"].search(
                [
                    ("partner_id", "=", request.env.user.partner_id.id),
                    ("state", "=", "sent"),
                ],
                order="date_order desc",
                limit=1,
            )
            if last_order:
                last_order.write({"state": "draft"})
                order = last_order

        request.session["website_sale_cart_quantity"] = (
            order.cart_quantity if order else 0
        )

        values = {
            "website_sale_order": order,
            "date": fields.Date.today(),
            "suggested_products": [],
        }

        if order:
            values.update(order._get_website_sale_extra_values())
            order.order_line.filtered(
                lambda line: line.product_id and not line.product_id.active
            ).unlink()
            values["suggested_products"] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        response.qcontext.update(values)
        return response

    @http.route(
        ["/shop/cart/update"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def cart_update(
        self,
        product_id,
        add_qty=1,
        set_qty=0,
        product_custom_attribute_values=None,
        no_variant_attribute_values=None,
        express=False,
        **kwargs,
    ):
        sale_order = super().cart_update(
            product_id=product_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            express=express,
            **kwargs,
        )

        request.session["website_sale_cart_quantity"] = sale_order.cart_quantity

        if express:
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")

    @http.route(
        ["/shop/cart/update_json"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def cart_update_json(
        self,
        product_id,
        line_id=None,
        add_qty=None,
        set_qty=None,
        display=True,
        product_custom_attribute_values=None,
        no_variant_attribute_values=None,
        **kw,
    ):
        values = super().cart_update_json(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            display=display,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kw,
        )

        request.session["website_sale_cart_quantity"] = values.get("cart_quantity", 0)

        return values
