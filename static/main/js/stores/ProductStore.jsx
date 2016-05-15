var assign = require('object-assign');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var ProductConstants = require('../constants/ProductConstants');
var EventEmitter = require('events').EventEmitter;

var _store = {
    metaData: {
        categories: [{
            name: ''
        }],
        products: [{
            id: 0,
            cost: 0,
            name: '',
            category: 0,
        }],
    }
}

var ProductStore = assign({}, EventEmitter.prototype, {
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
        case ProductConstants.PRODUCT_GET_DATA_RESPONSE:
            var response = action.response;
            _store.metaData = response;
            ProductStore.emitChange();
            break;

        default:
            // no op
    }
});

module.exports = ProductStore
