// Thanks to:
// http://owaislone.org/blog/webpack-plus-reactjs-and-django/

require('bootstrap/dist/css/bootstrap.css');

$ = jQuery = require('jquery');
React = require('react');

var ReactDOM = require('react-dom');
var NavigationBar = require('./NavigationBar');
var Menu = require('./Menu');

/* ReactDOM.render(<NavigationBar/>, document.getElementById('navigation')); */
ReactDOM.render(<Menu source="/api/menus/?format=json"/>, document.getElementById('menu'));
