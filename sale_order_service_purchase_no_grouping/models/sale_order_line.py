from odoo import _, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _purchase_service_generation(self):
        sale_line_purchase_map = {}
        for line in self:
            if line.product_id.product_tmpl_id.service_order_not_grouping:
                if line.product_id.service_to_purchase:
                    result = line._purchase_service_create()
                    sale_line_purchase_map.update(result)
            else:
                # Default behavior: check if purchase line count is zero before creating
                if line.product_id.service_to_purchase and not line.purchase_line_count:
                    result = line._purchase_service_create()
                    sale_line_purchase_map.update(result)
        return sale_line_purchase_map

    def _purchase_service_create(self, quantity=False):
        PurchaseOrder = self.env["purchase.order"]
        supplier_po_map = {}
        sale_line_purchase_map = {}
        for line in self:
            line = line.with_company(line.company_id)
            # determine vendor of the order (take the first matching company and product)
            suppliers = line.product_id._select_seller(
                quantity=line.product_uom_qty, uom_id=line.product_uom
            )
            if not suppliers:
                raise UserError(
                    _(
                        """There is no vendor associated to the product %s.
                        Please define a vendor for this product."""
                    )
                    % (line.product_id.display_name,)
                )
            supplierinfo = suppliers[0]
            partner_supplier = (
                supplierinfo.name
            )  # yes, this field is not explicit .... it is a res.partner !

            # determine (or create) PO
            purchase_order = None
            if not (
                line.product_id.product_tmpl_id.service_order_not_grouping
                and line.product_id.type == "service"
            ):
                purchase_order = supplier_po_map.get(partner_supplier.id)
                if not purchase_order:
                    purchase_order = PurchaseOrder.search(
                        [
                            ("partner_id", "=", partner_supplier.id),
                            ("state", "=", "draft"),
                            ("company_id", "=", line.company_id.id),
                        ],
                        limit=1,
                    )
            if not purchase_order:
                values = line._purchase_service_prepare_order_values(supplierinfo)
                purchase_order = PurchaseOrder.create(values)
            else:  # update origin of existing PO
                so_name = line.order_id.name
                origins = []
                if purchase_order.origin:
                    origins = purchase_order.origin.split(", ") + origins
                if so_name not in origins:
                    origins += [so_name]
                    purchase_order.write({"origin": ", ".join(origins)})
            supplier_po_map[partner_supplier.id] = purchase_order

            # add a PO line to the PO
            values = line._purchase_service_prepare_line_values(
                purchase_order, quantity=quantity
            )
            purchase_line = line.env["purchase.order.line"].create(values)

            # link the generated purchase to the SO line
            sale_line_purchase_map.setdefault(line, line.env["purchase.order.line"])
            sale_line_purchase_map[line] |= purchase_line
        return sale_line_purchase_map
