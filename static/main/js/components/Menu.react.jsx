// styles
require('menu.css');

// components
var DropdownButton = require('react-bootstrap').DropdownButton;
var MenuItem = require('react-bootstrap').MenuItem;
var Input = require('react-bootstrap').Input;

/* var Category = require('./Category.react');*/
var ProductList = require('./ProductList.react');

// actions
var MenuActions = require('../actions/MenuActions');
var ProductActions = require('../actions/ProductActions');

// stores
var MenuStore = require('../stores/MenuStore');

weekdays_accusative = ['понедельник',
                       'вторник',
                       'среду',
                       'четверг',
                       'пятницу',
                       'субботу',
                       'воскресение'];

var Menu = React.createClass({
    getMenuDataIfNeeded: function(props) {
        var meta = MenuStore.getState().metaData;

        if (props.activeMenu && props.activeMenu !== meta.id) {
            MenuActions.getMenuData();
        }
    },
    getInitialState: function() {
        return MenuStore.getState();
    },
    componentWillMount: function() {
        this.getMenuDataIfNeeded(this.props);
    },
    componentDidMount: function() {
        MenuStore.addChangeListener(this._onChange);
    },
    componentWillReceiveProps: function(nextProps) {
        this.getMenuDataIfNeeded(nextProps);
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
        MenuStore.removeChangeListener(this._onChange);
    },
    render: function() {
        if (typeof this.state.metaData.id == 'undefined') {
            return (
                <div className="menu">
                    <h1>Menu is loading...</h1>
                </div>
            )
        }

        var menu_id = this.state.metaData.id;
        var menu_data = this.state.metaData.menus[menu_id];
        var menu_pk = menu_data.id
        var menu_date = menu_data.date;
        var menu_weekday = menu_data.weekday;

        return (
            <div className="menu" data-forceid={menu_id}
                 data-forcedate={menu_date}>
                <h1>Меню на {weekdays_accusative[menu_weekday]}</h1>
                <ProductList activeMenu={menu_pk} />
            </div>
        )
    },
    _onChange: function() { this.setState(MenuStore.getState()); },
});

module.exports = Menu;
