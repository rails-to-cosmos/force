var API_URL = '/api';
var TIMEOUT = 10000;

var _pendingRequests = {};

var AppDispatcher = require('../dispatcher/AppDispatcher');
var MenuServerActions = require('../actions/MenuServerActions');
var MenuConstants = require('../constants/MenuConstants');
var request = require('superagent');


function abortPendingRequests(key) {
    if (_pendingRequests[key]) {
        _pendingRequests[key]._callback = function(){};
        _pendingRequests[key].abort();
        _pendingRequests[key] = null;
    }
}

function token() {
    return $.cookie('csrftoken');
}

function makeUrl(part) {
    return API_URL + part;
}

function dispatch(key, response, params) {
    /* var payload = {actionType: key, response: response};
     * if (params) {
     *     payload.queryParams = params;
     * }*/
    AppDispatcher.handleViewAction({
        actionType: MenuConstants.MENU_GET_DATA,
    });
}

// return successful response, else return request Constants
function makeDigestFun(key, params) {
    return function (err, res) {
        if (err && err.timeout === TIMEOUT) {
            dispatch(key, Constants.request.TIMEOUT, params);
        } else if (res.status === 400) {
            UserActions.logout();
        } else if (!res.ok) {
            dispatch(key, Constants.request.ERROR, params);
        } else {
            dispatch(key, res, params);
        }
    };
}

var MenuAPI = {
    getMenuData: function(entityId) {
        var url = makeUrl('/menus.json');
        var key = null; // Constants.api.GET_ENTITY_DATA;
        var params = null; // {entityId: entityId};
        abortPendingRequests(key);
        dispatch(key, MenuConstants.MENU_GET_DATA, params);
        _pendingRequests[key] = get(url).end(
            makeDigestFun(key, params)
        );
    }
};

module.exports = MenuAPI;

/* module.exports = {
 *   get: function() {
 *     request.get(makeUrl('menus.json'))
 *            .set('Accept', 'application/json')
 *            .end(function(err, response) {
 *                if (err) return console.error(err);
 *
 *                MenuServerActions.receiveMenuData(response.body);
 *            });
 *   }
 * };*/
