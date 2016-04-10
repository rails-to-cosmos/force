var AppDispatcher =  require('../dispatcher/AppDispatcher');
var MenuConstants = require('../constants/MenuConstants');
var MenuAPI = require('../utils/MenuAPI');


var MenuActions = {
    getMenuData: function() {
        AppDispatcher.handleViewAction({
            actionType: MenuConstants.MENU_GET_DATA,
        });

        MenuAPI.get();
    },
    order: function(menu, product) {
        AppDispatcher.dispatch({
            actionType: MenuConstants.MENU_ORDER,
            menu: menu,
            product: product,
        });
    },
    cancel: function(menu, product) {
        AppDispatcher.dispatch({
            actionType: MenuConstants.MENU_CANCEL,
            menu: menu,
            product: product,
        });
    },
    send: function(menu) {
        AppDispatcher.dispatch({
            actionType: MenuConstants.MENU_GET_DATA,
            menu: menu,
        });
    }
}

module.exports = MenuActions;
