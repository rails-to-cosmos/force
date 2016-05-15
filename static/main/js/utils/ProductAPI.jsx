var ProductServerActions = require('../actions/ProductServerActions');
var request = require('superagent');

module.exports = {
  get: function(menu_id) {
    request.get('/api/menus/' + menu_id + '/products.json')
      .set('Accept', 'application/json')
      .end(function(err, response) {
        if (err) return console.error(err);

        ProductServerActions.receiveProductData(response.body);
      });
  }
};
