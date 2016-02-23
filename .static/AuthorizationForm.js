Login = React.createClass({displayName: "Login",
    init: function() {
        this.state = {
            user: '',
            password: ''
        }
    },
    render: function() {
        return (
            React.createElement("div", {className: "loginForm"}, 
                "login here"
            )
        )
    }
})

var AuthorizationForm = React.createClass({displayName: "AuthorizationForm",
    render: function() {
        return (
            React.createElement("div", {className: "authorizationFormContainer"}, 
            React.createElement(Input, {type: "text", bsSize: "small", placeholder: "Login"}), 
            React.createElement(Input, {type: "password", bsSize: "small", placeholder: "Password"}), 
            React.createElement(Button, {type: "submit", bsStyle: "success", bsSize: "small"}, "Login")
            )
        );
    }
});
