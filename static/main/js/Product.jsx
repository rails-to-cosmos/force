var Name = React.createClass({
    getDefaultProps: function() {
        return {
            value: ''
        };
    },
    render: function() {
        return (<p className="productName"><strong>{this.props.value}</strong></p>)
    }
});

var Cost = React.createClass({
    getDefaultProps: function() {
        return {
            value: ''
        };
    },
    render: function() {
        return (<span className="productCost">{this.props.value} ₽</span>)
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
        return (
            <div key={this.props.key} className="product">
                <Name value={this.props.name}/>
                <p>
                    <Description value={this.props.description}/> <Cost value={this.props.cost}/>
                </p>
            </div>
        )
    }
});


module.exports = Product;
