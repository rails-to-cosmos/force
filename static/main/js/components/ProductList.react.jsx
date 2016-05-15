var ProductStore = require('../stores/ProductStore');
var ProductActions = require('../actions/ProductActions');

var ProductList = React.createClass({
    getProductDataIfNeeded: function(props) {
        var meta = ProductStore.getState().metaData;

        if (props.activeMenu && props.activeMenu !== meta.activeMenu) {
            ProductActions.getProductData(props.activeMenu);
        }
    },
    getInitialState: function() {
        return ProductStore.getState();
    },
    componentWillMount: function() {
        this.getProductDataIfNeeded(this.props);
    },
    componentDidMount: function() {
        ProductStore.addChangeListener(this._onChange);
    },
    componentWillReceiveProps: function(nextProps) {
        this.getProductDataIfNeeded(nextProps);
    },
    componentWillUnmount: function() {
        this.serverRequest.abort();
        ProductStore.removeChangeListener(this._onChange);
    },
    render: function() {
        return (
            <div className="productList">
                Product list is here
            </div>
        )
    },
    _onChange: function() { this.setState(ProductStore.getState()); },
});

module.exports = ProductList;
