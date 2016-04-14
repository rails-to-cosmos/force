// Thanks to:
// http://owaislone.org/blog/webpack-plus-reactjs-and-django/

require('bootstrap/dist/css/bootstrap.css');

$ = jQuery = require('jquery');
React = require('react');

var ReactDOM = require('react-dom');
var NavigationBar = require('./NavigationBar');
var Menu = require('./components/Menu.react');

ReactDOM.render(<NavigationBar />,
                document.getElementById('navigation'));

ReactDOM.render(<Menu source="/api/menus.json"/>,
                document.getElementById('menu'));
