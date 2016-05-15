require('jquery.cookie');

var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var Button = require('react-bootstrap').Button;
var Input = require('react-bootstrap').Input;
var AuthorizationForm = React.createClass({
    getInitialState: function() {
        state = {
            authorized: false,
            fullname: ''
        }

        return state
    },
    setUnauthorizedState: function() {
        this.setState({
            fullname: '',
            authorized: false
        });
    },
    componentDidMount: function() {
        this.serverRequest = $.get(this.props.source, function(result) {
            if (result.unauthorized) {
                this.setUnauthorizedState();
            } else {
                this.setState({
                    fullname: result.first_name + ' ' + result.last_name,
                    authorized: true
                });
            }
        }.bind(this)).fail(function() {
            this.setUnauthorizedState();
        }.bind(this));
    },
    login: function() {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/auth/login/',
            data: {
                username: this.state.username,
                password: this.state.password,
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            success: function(data) {
                this.setState({
                    username: '',
                    password: '',
                    authorized: true,
                    fullname: data.fullname,
                    passwordValidationState: undefined,
                });
            }.bind(this),
            error: function(xhr, status, err) {
                this.setState({
                    username: this.state.username,
                    password: this.state.password,
                    authorized: false,
                    passwordValidationState: 'error',
                });
            }.bind(this)
        });
    },
    logout: function(e) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/auth/logout/',
            data: {
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            success: function(data) {
                this.setUnauthorizedState();
            }.bind(this),
            error: function(xhr, status, err) {
                console.log('error on exit');
            }.bind(this)
        });
    },
    updateUsername: function(event) {
        this.state.username = event.target.value;
    },
    updatePassword: function(event) {
        this.state.password = event.target.value;
    },
    maybeSendForm: function(event) {
        if (event.key == 'Enter') {
            this.login();
        }
    },
    render: function() {
        if (this.state.authorized) {
            return (
                <Navbar.Collapse>
                    <Navbar.Form pullRight>
                        <Button onClick={this.logout}
                                type="button"
                                bsStyle="danger"
                                bsSize="small">Выход</Button>
                    </Navbar.Form>
                    <Navbar.Text pullRight>
                        Добро пожаловать, <Navbar.Link href="#">{this.state.fullname}</Navbar.Link>
                    </Navbar.Text>
                </Navbar.Collapse>
            );
        } else {
            return (
                <Navbar.Form pullRight>
                    <Input ref="username"
                           type="text"
                           bsSize="small"
                           placeholder="Имя пользователя"
                           defaultValue={this.state.username}
                           onChange={this.updateUsername}
                           autoFocus="True"
                           onKeyDown={this.maybeSendForm}/>
                    {' '}
                    <Input ref="password"
                           type="password"
                           bsStyle={this.state.passwordValidationState}
                           bsSize="small"
                           placeholder="Пароль"
                           defaultValue={this.state.password}
                           onChange={this.updatePassword}
                           onKeyDown={this.maybeSendForm}/>
                    {' '}
                    <Button onClick={this.login}
                            type="button"
                            bsStyle="success"
                            bsSize="small">Вход</Button>
                </Navbar.Form>
            );
        }
    }
});

module.exports = AuthorizationForm;
