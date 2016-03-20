var Product = require('./Product');
var Category = React.createClass({
    getDefaultProps: function() {
        return {
            value: 'default category'
        };
    },
    render: function() {
        return (
            <div key={this.props.key} className="category">
                <h4>{this.props.value}</h4>
                {this.props.products.map(function(product){
                     return (
                         <Product key={product.id}
                                  name={product.name}
                                  description={product.description}
                                  cost={product.cost}/>
                     )
                 })}
            </div>
        )
    }
});


module.exports = Category;
