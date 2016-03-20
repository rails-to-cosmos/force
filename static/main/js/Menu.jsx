require('menu.css');

var Category = require('./Category');
var Menu = React.createClass({
    render: function() {
        return (
            <div className="menu">
                <h3>Меню на понедельник</h3>
                {
                    this.props.products.map(function(category){
                        return (<Category key={category[0]}
                                          value={category[1]}
                                          products={category[2]}/>);
                    })
                }
            </div>
        )
    }
});

module.exports = Menu;
