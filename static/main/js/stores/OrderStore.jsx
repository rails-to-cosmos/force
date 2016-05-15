var assign = require('object-assign');
var EventEmitter = require('events').EventEmitter;
var AppDispatcher = require('../dispatcher/AppDispatcher');


var _store = {
    orders: [],
}

var OrderStore = assign({}, EventEmitter.prototype, {
    CHANGE_EVENT: 'change',

    getOrderData: function() {
        return _store;
    },

    emitChange: function() {
        this.emit(this.CHANGE_EVENT);
    },

    addChangeListener: function(callback) {
        this.on(this.CHANGE_EVENT, callback);
    },

    removeChangeListener: function(callback) {
        this.removeListener(this.CHANGE_EVENT, callback);
    },
});

function makeOrder(menu, product, count) {
    var id = (+new Date() + Math.floor(Math.random() * 999999)).toString(36);
    _orders[id] = {
        id: id,
        product: product,
        menu: menu,
        count: count,
    }
}

function cancelOrder(id) {
    delete _store.orders[id];
}

// Register callback to handle all updates
AppDispatcher.register(function(payload) {
    var action = payload.action;

    switch(action.actionType) {
        case MenuConstants.MENU_GET_DATA_RESPONSE:
            var response = action.response;
            _store.menus = response;
            _store.current_menu = 0;
            MenuStore.emitChange();
            break;

            /* case MenuConstants.MENU_ORDER:
             *     makeOrder(action.menu, action.product, count);
             *     MenuStore.emitChange();
             *     break;

             * case MenuConstants.MENU_CANCEL:
             *     cancelOrder(action.menu, action.product);
             *     MenuStore.emitChange();
             *     break;*/

        case MenuConstants.MENU_SEND:
            break;

        default:
            // no op
    }
});

module.exports = OrderStore
