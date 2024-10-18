import logging

from odoo import SUPERUSER_ID, fields, http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route(["/shop/cart"], type="http", auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive="", **post):
        _logger.info(
            "Entrando a la función cart con access_token: %s y revive: %s",
            access_token,
            revive,
        )

        SaleOrder = request.env["sale.order"].sudo()
        sale_order_id = request.session.get("sale_order_id")
        _logger.debug("ID del pedido en la sesión: %s", sale_order_id)

        if sale_order_id:
            sale_order_sudo = SaleOrder.browse(sale_order_id).exists()
            _logger.debug("Pedido encontrado en la sesión: %s", sale_order_sudo)
        elif request.env.user and not request.env.user._is_public():
            sale_order_sudo = request.env.user.partner_id.last_website_so_id
            _logger.debug("Pedido encontrado para el usuario: %s", sale_order_sudo)

            if sale_order_sudo:
                available_pricelists = self.get_pricelist_available()
                _logger.debug("Listas de precios disponibles: %s", available_pricelists)

                if sale_order_sudo.pricelist_id not in available_pricelists:
                    _logger.warning(
                        "La lista de precios del pedido no está disponible."
                    )
                    sale_order_sudo = None
                else:
                    fpos = (
                        sale_order_sudo.env["account.fiscal.position"]
                        .with_company(sale_order_sudo.company_id)
                        ._get_fiscal_position(
                            sale_order_sudo.partner_id,
                            delivery=sale_order_sudo.partner_shipping_id,
                        )
                    )
                    _logger.debug("Posición fiscal obtenida: %s", fpos)
                    if fpos.id != sale_order_sudo.fiscal_position_id.id:
                        _logger.warning(
                            "La posición fiscal ha cambiado, invalidando el pedido."
                        )
                        sale_order_sudo = None
        else:
            sale_order_sudo = SaleOrder
            _logger.debug("No se encontró un pedido previo, se creará uno nuevo.")

        if sale_order_sudo and sale_order_sudo.state in (
            "pending",
            "authorized",
            "done",
        ):
            _logger.warning(
                "El pedido está en un estado no válido: %s", sale_order_sudo.state
            )
            sale_order_sudo = None

        if sale_order_sudo and sale_order_sudo.state not in ["draft", "sent"]:
            _logger.info(
                "El pedido tiene un estado diferente de 'draft' y 'sent',\
                    reiniciando el ID del pedido en la sesión."
            )
            request.session["sale_order_id"] = None
            sale_order_sudo = SaleOrder

        if not sale_order_sudo:
            partner_sudo = request.env.user.partner_id
            _logger.info("Creando un nuevo pedido para el socio: %s", partner_sudo.name)

            website = request.env['website'].get_current_website()

            so_data = website._prepare_sale_order_values(partner_sudo)

            sale_order_sudo = SaleOrder.with_user(SUPERUSER_ID).create(so_data)

            request.session["sale_order_id"] = sale_order_sudo.id
            request.session["website_sale_cart_quantity"] = sale_order_sudo.cart_quantity
            sale_order_sudo = sale_order_sudo.with_user(request.env.user).sudo()

        _logger.debug(
            "Cantidad del carrito antes de la actualización: %s",
            request.session.get("website_sale_cart_quantity", 0),
        )
        request.session["website_sale_cart_quantity"] = sale_order_sudo.cart_quantity

        values = {
            "website_sale_order": sale_order_sudo,
            "date": fields.Date.today(),
            "suggested_products": [],
        }

        if sale_order_sudo:
            _logger.info("Actualizando valores adicionales para el pedido.")
            values.update(sale_order_sudo._get_website_sale_extra_values())

            _logger.debug(
                "Líneas del pedido antes de limpiar: %s", sale_order_sudo.order_line
            )
            sale_order_sudo.order_line.filtered(
                lambda line: line.product_id and not line.product_id.active
            ).unlink()
            _logger.info("Líneas inactivas eliminadas del pedido.")

            _logger.info("Calculando productos sugeridos para el pedido.")
            values["suggested_products"] = sale_order_sudo._cart_accessories()
            values.update(self._get_express_shop_payment_values(sale_order_sudo))

        response = super().cart(access_token=access_token, revive=revive, **post)
        response.qcontext.update(values)

        _logger.info("Valores de respuesta actualizados: %s", values)
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
        **kwargs
    ):
        _logger.info(
            "Actualizando carrito con producto_id: %s, add_qty: %s, set_qty: %s",
            product_id,
            add_qty,
            set_qty,
        )

        sale_order = super().cart_update(
            product_id=product_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            express=express,
            **kwargs
        )

        request.session["website_sale_cart_quantity"] = sale_order.cart_quantity
        _logger.info("Cantidad del carrito actualizada a: %s", sale_order.cart_quantity)

        if express:
            _logger.info("Redirigiendo a la página de checkout en modo expreso.")
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
        **kw
    ):
        _logger.info(
            "Actualizando carrito (JSON) con producto_id: %s,\
            line_id: %s, add_qty: %s, set_qty: %s",
            product_id,
            line_id,
            add_qty,
            set_qty,
        )

        values = super().cart_update_json(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            display=display,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kw
        )

        request.session["website_sale_cart_quantity"] = values.get("cart_quantity", 0)
        _logger.info(
            "Cantidad del carrito actualizada a: %s", values.get("cart_quantity", 0)
        )

        return values
