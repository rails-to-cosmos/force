Login = React.createClass({
    init: function() {
        this.state = {
            user: '',
            password: ''
        }
    },
    render: function() {
        return (
            <div className="loginForm">
                login here
            </div>
        )
    }
})

var AuthorizationForm = React.createClass({
    render: function() {
        return (
            <div className="authorizationFormContainer">
            <Input type="text" bsSize="small" placeholder="Login"/>
            <Input type="password" bsSize="small" placeholder="Password"/>
            <Button type="submit" bsStyle="success" bsSize="small">Login</Button>
            </div>
        );
    }
});
