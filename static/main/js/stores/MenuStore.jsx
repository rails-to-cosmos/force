var AppDispatcher = require('../dispatcher/AppDispatcher');
var MenuConstants = require('../constants/MenuConstants');
var assign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var _store = {
    menus: [{
        id: 0,
        date: '',
        orders: [],
        products: [],
    }],
    orders: [],
    current_menu: 0,
}

var CHANGE_EVENT = 'change';


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

var MenuStore = assign({}, EventEmitter.prototype, {
    getMenuData: function() {
        return _store;
    },

    emitChange: function() {
        this.emit(CHANGE_EVENT);
    },

    addChangeListener: function(callback) {
        this.on(CHANGE_EVENT, callback);
    },

    removeChangeListener: function(callback) {
        this.removeListener(CHANGE_EVENT, callback);
    },
});

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

        case MenuConstants.MENU_ORDER:
            makeOrder(action.menu, action.product, count);
            MenuStore.emitChange();
            break;

        case MenuConstants.MENU_CANCEL:
            cancelOrder(action.menu, action.product);
            MenuStore.emitChange();
            break;

        case MenuConstants.MENU_SEND:
            break;

        default:
            // no op
    }
});

module.exports = MenuStore;
