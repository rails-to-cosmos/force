var AppDispatcher =  require('../dispatcher/AppDispatcher');
var ProductConstants = require('../constants/ProductConstants');
var ProductAPI = require('../utils/ProductAPI');

var ProductActions = {
    getProductData: function(menu_id) {
        AppDispatcher.handleViewAction({
            actionType: ProductConstants.PRODUCT_GET_DATA,
        });

        ProductAPI.get(menu_id);
    },
    send: function(product) {
        AppDispatcher.dispatch({
            actionType: ProductConstants.PRODUCT_GET_DATA,
            product: product,
        });
    }
}

module.exports = ProductActions;
