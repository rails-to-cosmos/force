var assign = require('object-assign');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var MenuConstants = require('../constants/MenuConstants');
var EventEmitter = require('events').EventEmitter;

var _store = {
    metaData: {

    }
}

var MenuStore = assign({}, EventEmitter.prototype, {
    CHANGE_EVENT: 'change',

    getState: function() {
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

// Register callback to handle all updates
AppDispatcher.register(function(payload) {
    var action = payload.action;

    switch(action.actionType) {
        case MenuConstants.MENU_GET_DATA_RESPONSE:
            var response = action.response;
            _store.metaData.menus = response;
            _store.metaData.id = 0;
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

module.exports = MenuStore;
