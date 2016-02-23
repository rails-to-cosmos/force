var ProductList = React.createClass({displayName: "ProductList",
  render: function() {
    return (
      React.createElement("div", {className: "productList"}, 
        "Hello there. I'm a React component."
      )
    );
  }
});
ReactDOM.render(
  React.createElement(ProductList, null),
  document.getElementById('content')
);
