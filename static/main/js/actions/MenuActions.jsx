var AppDispatcher = require('../dispatcher/AppDispatcher');
var MenuConstants = require('../constants/MenuConstants');
var MenuAPI = require('../utils/MenuAPI');

var MenuActions = {
    getMenuData: function() {
        MenuAPI.getMenuData();
        /* AppDispatcher.handleViewAction({
         *     actionType: MenuConstants.MENU_GET_DATA,
         * });
         */
    },
    /* send: function(menu) {
     *     AppDispatcher.dispatch({
     *         actionType: MenuConstants.MENU_GET_DATA,
     *         menu: menu,
     *     });
     * },*/
    /* order: function(menu, product) {
     *     AppDispatcher.dispatch({
     *         actionType: MenuConstants.MENU_ORDER,
     *         menu: menu,
     *         product: product,
     *     });
     * },
     * cancel: function(menu, product) {
     *     AppDispatcher.dispatch({
     *         actionType: MenuConstants.MENU_CANCEL,
     *         menu: menu,
     *         product: product,
     *     });
     * },*/
}

module.exports = MenuActions;
