var ProductList = React.createClass({
  render: function() {
    return (
      <div className="productList">
        Hello there. I'm a React component.
      </div>
    );
  }
});
ReactDOM.render(
  <ProductList />,
  document.getElementById('content')
);
