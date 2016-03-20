require('jquery.cookie');

var Button = require('react-bootstrap').Button;
var Input = require('react-bootstrap').Input;
var AuthorizationForm = React.createClass({
    getInitialState: function() {
        console.log(_appData);

        state = {
            authorized: _appData.user.id != 'None',
        }

        if (state.authorized) {
            state.fullname = _appData.user.fullname;
        }

        return state
    },
    login: function() {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: '/auth/',
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
            url: '/auth/logout',
            data: {
                csrfmiddlewaretoken: $.cookie('csrftoken')
            },
            success: function(data) {
                this.setState({
                    username: '',
                    password: '',
                    authorized: false,
                    passwordValidationState: undefined,
                });
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
                <form className="authorizationFormContainer">
                    <span className="greetings">
                        Добро пожаловать, <a href="#">{this.state.fullname}</a>
                    </span>
                    <Button onClick={this.logout}
                            type="button"
                            bsStyle="danger"
                            bsSize="small">Выход</Button>
                </form>
            );
        } else {
            return (
                <form className="authorizationFormContainer">
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
                </form>
            );
        }
    }
});

module.exports = AuthorizationForm;
