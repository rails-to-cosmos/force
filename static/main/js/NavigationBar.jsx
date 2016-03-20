var Navbar = require('react-bootstrap').Navbar;
var AuthorizationForm = require('./AuthorizationForm')
var NavigationBar = React.createClass({
    render: function() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Navbar.Form pullRight>
                        <AuthorizationForm />
                    </Navbar.Form>
                </Navbar.Collapse>
            </Navbar>
        );
    }
});

module.exports = NavigationBar;
