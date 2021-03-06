var Product = require('./Product.react');
var Category = React.createClass({
    render: function() {
        return (
            <div key={this.props.key} className="category">
                <h4 key={this.props.key}>{this.props.value}</h4>
                {this.props.products.map(function(product){
                     return (
                         <Product key={product.id}
                                  id={product.id}
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
