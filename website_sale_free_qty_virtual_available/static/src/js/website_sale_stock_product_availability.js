odoo.define("website_sale_free_qty_virtual_available.VariantMixin", function (require) {
  "use strict";

  var VariantMixin = require("website_sale_stock.VariantMixin");

  var originalFunction = VariantMixin._onChangeCombinationStock;

  VariantMixin._onChangeCombinationStock = function (ev, $parent, combination) {
    // originalFunction.apply(this, arguments);

    if (combination && combination.product_id) {
      var virtualAvailable = combination.virtual_available || 0;

      var $input = $parent.find('input[name="add_qty"]');
      if ($input.length && parseFloat($input.val()) > virtualAvailable) {
        $input.val(virtualAvailable);
      }

      var $stockWarning = $parent.find(".availability_message");
      if ($stockWarning.length) {
        var message =
          virtualAvailable > 0
            ? _.str.sprintf("Only %s units available in stock.", virtualAvailable)
            : "Out of stock";
        $stockWarning.html(message);
      }
    }
    if (
      combination.product_type === "product" &&
      !combination.allow_out_of_stock_order
    ) {
      combination.virtual_available -= parseInt(combination.cart_qty);
      const $addQtyInput = $parent.find('input[name="add_qty"]');
      let qty = $addQtyInput.val();
      const ctaWrapper = $parent[0].querySelector("#o_wsale_cta_wrapper");
      ctaWrapper.classList.replace("d-none", "d-flex");
      ctaWrapper.classList.remove("out_of_stock");

      $addQtyInput.data("max", combination.virtual_available || 1);
      if (combination.virtual_available < 0) {
        combination.virtual_available = 0;
      }
      if (qty > combination.virtual_available) {
        qty = combination.virtual_available || 1;
        $addQtyInput.val(qty);
      }
      if (combination.virtual_available < 1) {
        ctaWrapper.classList.replace("d-flex", "d-none");
        ctaWrapper.classList.add("out_of_stock");
      }
    }
  };
});
