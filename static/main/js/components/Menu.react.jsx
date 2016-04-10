var DropdownButton = require('react-bootstrap').DropdownButton;
var MenuItem = require('react-bootstrap').MenuItem;
var Input = require('react-bootstrap').Input;

require('menu.css');
var Category = require('./Category.react');

var MenuActions = require('../actions/MenuActions');
var MenuStore = require('../stores/MenuStore');


function getMenuState() {
    var menuData = MenuStore.getMenuData();
    var currentMenu = menuData.menus[menuData.current_menu]

    var menuState = {
        id: currentMenu.id,
        date: currentMenu.date,
        orders: currentMenu.orders,
        products: currentMenu.products,
    }

    // TODO 3 times here on initialize. WTF?
    return menuState;
}

var Menu = React.createClass({
    getInitialState: function() {
        return getMenuState();
    },
    componentDidMount: function() {
        MenuActions.getMenuData();
        MenuStore.addChangeListener(this._onChange);
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        return (
            <div className="menu"
                 data-forceid={this.state.id}
                 data-forcedate={this.state.date}>
                {/* {
                Object.keys(this.state.products).map(function(category){
                return (<Category key={category}
                value={this.state.categories[category]}
                products={this.state.products[category]}/>);
                }.bind(this))
                } */}
            </div>
        )
    },
    _onChange: function() {
        this.setState(getMenuState);
    },
});

module.exports = Menu;
