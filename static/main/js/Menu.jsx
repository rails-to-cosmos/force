require('menu.css');

var DropdownButton = require('react-bootstrap').DropdownButton;
var MenuItem = require('react-bootstrap').MenuItem;
var Category = require('./Category');
var Input = require('react-bootstrap').Input;
var Menu = React.createClass({
    getInitialState: function() {
        return {
            'id': '',
            'date': '',
            'products': {},
        }
    },
    componentDidMount: function() {
        this.serverRequest = $.get(this.props.source, function(result) {
            mbw = {}; // menus grouped by weekday
            cats = {};

            for (menu in result) {
                if (typeof mbw[result[menu]['weekday']] == 'undefined') {
                    mbw[result[menu]['weekday']] = [];
                }

                pbc = {}; // products grouped by category
                for (pi in result[menu]['products']) {
                    if (typeof pbc[result[menu]['products'][pi]['category']] == 'undefined') {
                        pbc[result[menu]['products'][pi]['category']] = [];
                        cats[result[menu]['products'][pi]['category']] = result[menu]['products'][pi]['category_name']
                    }
                    pbc[result[menu]['products'][pi]['category']].push({
                        id: result[menu]['products'][pi]['id'],
                        compound: result[menu]['products'][pi]['compound'],
                        cost: result[menu]['products'][pi]['cost'],
                        name: result[menu]['products'][pi]['name'],
                        weight: result[menu]['products'][pi]['weight'],
                    });
                }

                mbw[result[menu]['weekday']] = {
                    id: result[menu]['id'],
                    date: result[menu]['date'],
                    products: pbc,
                    categories: cats,
                };
            }

            defaultMenu = mbw[0];
            this.setState({
                id: defaultMenu['id'],
                date: defaultMenu['date'],
                weekday: defaultMenu['weekday'],
                products: pbc,
                categories: cats,
            });

            console.log(defaultMenu);
        }.bind(this));
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
    },
    render: function() {
        return (
            <div className="menu" data-forceid={this.state.id} data-forcedate={this.state.date}>
                Меню на <DropdownButton bsStyle="link" title="понедельник" eventKey={1} id="0">
                <MenuItem eventKey={0}>понедельник</MenuItem>
                <MenuItem eventKey={1}>вторник</MenuItem>
                <MenuItem eventKey={2}>среду</MenuItem>
                <MenuItem eventKey={3}>четверг</MenuItem>
                <MenuItem eventKey={4}>пятницу</MenuItem>
                <MenuItem eventKey={5}>субботу</MenuItem>
                <MenuItem eventKey={6}>воскресенье</MenuItem>
                </DropdownButton>

                {
                    Object.keys(this.state.products).map(function(category){
                        return (<Category key={category}
                                          value={this.state.categories[category]}
                                          products={this.state.products[category]}/>);
                    }.bind(this))
                }
            </div>
        )
    }
});

module.exports = Menu;
