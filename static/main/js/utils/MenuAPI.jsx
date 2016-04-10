var MenuServerActions = require('../actions/MenuServerActions');
var request = require('superagent');

module.exports = {
  get: function() {
    request.get('/api/menus.json')
      .set('Accept', 'application/json')
      .end(function(err, response) {
        if (err) return console.error(err);

        MenuServerActions.receiveMenuData(response.body);
      });
  }
};
