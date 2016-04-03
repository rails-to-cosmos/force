var Navbar = require('react-bootstrap').Navbar;
var Nav = require('react-bootstrap').Nav;
var NavItem = require('react-bootstrap').NavItem;
var NavDropdown = require('react-bootstrap').NavDropdown;
var MenuItem = require('react-bootstrap').MenuItem;
var Badge = require('react-bootstrap').Badge;


var AuthorizationForm = require('./AuthorizationForm')
    var NavigationBar = React.createClass({
        render: function() {
            return (
                <Navbar>
                    <Navbar.Header>
                        <Navbar.Brand>
                            <a href="#">СИЗО <sup>с тобой до конца</sup></a>
                        </Navbar.Brand>
                    </Navbar.Header>
                    <Nav>
                        <NavDropdown eventKey={1} title="Админские примочки" id="basic-nav-dropdown">
                            <MenuItem eventKey={1.6}>Оповещение: Привезли обеды</MenuItem>
                            <MenuItem eventKey={1.7}>Оповещение: Деньги за обеды</MenuItem>
                            <MenuItem eventKey={1.8}>Оповещение: Отправка через 10 минут</MenuItem>
                            <MenuItem divider />
                            <MenuItem eventKey={1.4}>Загрузить меню на следующую неделю</MenuItem>
                            <MenuItem eventKey={1.5}>Отправить меню</MenuItem>
                            <MenuItem eventKey={1.5}>Отправить меню через десять минут</MenuItem>
                            <MenuItem eventKey={1.5}>Отложить отправку меню на пять минут</MenuItem>
                            <MenuItem eventKey={1.1}>Закрыть меню</MenuItem>
                            <MenuItem divider />
                            <MenuItem eventKey={1.2}>Заказы на сегодня</MenuItem>
                            <MenuItem eventKey={1.3}>Неоплаченные заказы (1)</MenuItem>
                            <MenuItem divider />
                            <MenuItem eventKey={1.4}>Поставщики</MenuItem>
                        </NavDropdown>
                        <NavItem eventKey={1} href="#">Мои заказы</NavItem>
                        <NavItem eventKey={1} href="#">Чек <Badge className="force-nobold">200 &#8381;</Badge></NavItem>
                    </Nav>
                    <AuthorizationForm />
                </Navbar>
            );
        }
    });

module.exports = NavigationBar;
