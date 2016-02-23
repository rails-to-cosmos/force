const mountNode = document.getElementById('navigation');

Navbar = ReactBootstrap.Navbar;
Button = ReactBootstrap.Button;
Input = ReactBootstrap.Input;

const navbarInstance = (
  React.createElement(Navbar, {bsStyle: "inverse"}, 
    React.createElement(Navbar.Header, null, 
      React.createElement(Navbar.Toggle, null)
    ), 
    React.createElement(Navbar.Collapse, null, 
      React.createElement(Navbar.Form, {pullLeft: true}, 
        React.createElement(Input, {type: "text", placeholder: "Search"}), 
        ' ', 
        React.createElement(Button, {type: "submit"}, "Submit")
      ), 
      React.createElement(Navbar.Form, {pullRight: true}, 
          React.createElement(AuthorizationForm, null)
      )
    )
  )
);

ReactDOM.render(navbarInstance, mountNode);
