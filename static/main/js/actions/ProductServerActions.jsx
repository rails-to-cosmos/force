var AppDispatcher =  require('../dispatcher/AppDispatcher');
var ProductConstants = require('../constants/ProductConstants');

var ProductServerActions = {
    receiveProductData: function(response) {
        AppDispatcher.handleServerAction({
            actionType: ProductConstants.PRODUCT_GET_DATA_RESPONSE,
            response: response
        });
    },
}

module.exports = ProductServerActions;
