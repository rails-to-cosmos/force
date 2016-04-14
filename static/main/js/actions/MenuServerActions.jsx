var AppDispatcher =  require('../dispatcher/AppDispatcher');
var MenuConstants = require('../constants/MenuConstants');

var MenuServerActions = {
    receiveMenuData: function(response) {
        AppDispatcher.handleServerAction({
            actionType: MenuConstants.MENU_GET_DATA_RESPONSE,
            response: response
        });
    },
}

module.exports = MenuServerActions;
