const mountNode = document.getElementById('navigation');

Navbar = ReactBootstrap.Navbar;
Button = ReactBootstrap.Button;
Input = ReactBootstrap.Input;

const searchForm = (
    <Navbar.Form pullLeft>
        <Input type="text" placeholder="Search"/>
        {' '}
        <Button type="submit">Submit</Button>
    </Navbar.Form>
)

const navbarInstance = (
  <Navbar bsStyle="inverse">
    <Navbar.Header>
      <Navbar.Toggle />
    </Navbar.Header>
    <Navbar.Collapse>
      <Navbar.Form pullLeft>
          <AuthorizationForm />
      </Navbar.Form>
    </Navbar.Collapse>
  </Navbar>
);

ReactDOM.render(navbarInstance, mountNode);
