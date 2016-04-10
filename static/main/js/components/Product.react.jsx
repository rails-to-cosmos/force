var ProductName = React.createClass({
    render: function() {
        return (
            <dt className="productName">
                <span className="productNameInner">{this.props.value}</span>
            </dt>
        )
    }
});

var ProductCost = React.createClass({
    render: function() {
        return (
            <dd className="productCost">
                <span className="productCostInner">{this.props.value}&nbsp;₽</span>
            </dd>
        )
    }
});

var ProductDescription = React.createClass({
    render: function() {
        return (
            <span className="productDescription">{this.props.value}</span>
        )
    }
});

var Product = React.createClass({
    order: function() {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/api/orders/',
            data: {
                product: this.props.id,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            success: function(data) {
                MenuStore.getOrders();
            }.bind(this),
            error: function(xhr, status, err) {
                MenuStore.getOrders();
            }.bind(this)
        });
    },
    render: function() {
        return (
            <dl key={this.props.key} className="product" id={this.props.id} onClick={this.order}>
                <ProductName value={this.props.name}/><ProductCost value={this.props.cost}/>
            </dl>
        )
    }
});

module.exports = Product;
