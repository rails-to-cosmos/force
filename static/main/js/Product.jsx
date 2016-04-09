var Name = React.createClass({
    getDefaultProps: function() {
        return {
            value: ''
        };
    },
    render: function() {
        return (<dt className="productName"><span className="productNameInner">{this.props.value}</span></dt>)
    }
});

var Cost = React.createClass({
    getDefaultProps: function() {
        return {
            value: ''
        };
    },
    render: function() {
        return (<dd className="productCost"><span className="productCostInner">{this.props.value}&nbsp;₽</span></dd>)
    }
});

var Description = React.createClass({
    getDefaultProps: function() {
        return {
            value: ''
        };
    },
    render: function() {
        return (<span className="productDescription">{this.props.value}</span>)
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

            }.bind(this),
            error: function(xhr, status, err) {

            }.bind(this)
        });
    },
    render: function() {
        return (
            <dl key={this.props.key} className="product" id={this.props.id} onClick={this.order}>
                <Name value={this.props.name}/><Cost value={this.props.cost}/>
            </dl>
        )
    }
});


module.exports = Product;
