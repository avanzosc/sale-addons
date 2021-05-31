odoo.define('inherit_event_sale.product_configurator', function (require) {
"use strict";

    var ProductConfiguratorWidget = require('event_sale.product_configurator');

    ProductConfiguratorWidget.include({
        _checkForEvent: function (productId, dataPointId) {
            var self = this;
            return this._rpc({
                model: 'product.product',
                method: 'read',
                args: [productId, ['event_ok']],
            }).then(function (result) {
                if (Array.isArray(result) && result.length && result[0].event_ok) {
                    /**
                    self._openEventConfigurator({
                            default_product_id: productId
                        },
                        dataPointId
                    );
                    */
                    return Promise.resolve(true);
                }
                return Promise.resolve(false);
            });
        },
    });
});
