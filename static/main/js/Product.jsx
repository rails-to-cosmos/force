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
    getDefaultProps: function() {
        return {
            key: '',
            name: '',
            description: '',
            cost: '',
        }
    },
    render: function() {
        {/* <Description value={this.props.description}/> */}
        return (
            <dl key={this.props.key} className="product">
                <Name value={this.props.name}/><Cost value={this.props.cost}/>
            </dl>
        )
    }
});


module.exports = Product;
