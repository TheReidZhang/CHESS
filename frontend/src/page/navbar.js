import React, {useState, useEffect} from 'react';
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar'
import NavDropdown from 'react-bootstrap/NavDropdown'
import 'bootstrap/dist/css/bootstrap.min.css';
import {useHistory} from 'react-router-dom';


function Navigation(props) {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, setUserName] = useState("");
    useEffect(() => {
        (async function runEffect() {
            const response = await fetch('/user');
            const json = await response.json();
            if (json["valid"]) {
                setIsLoggedIn(true);
                setUserName(json["username"]);
            }
        })();
    }, []);

    const history = useHistory();
    const logout = async() => {
        await fetch('/logout');
        history.go(0);
    }

    const renderButton = () => {
        if (isLoggedIn) {
            return (
                <NavDropdown title={userName} flip alignRight id="basic-nav-dropdown" style={{minWidth: "auto"}}>
                    <NavDropdown.Item>
                        <div style={{textAlign: "center", fontSize: "50%", fontWeight: "bold"}}>
                            Profile
                        </div>
                    </NavDropdown.Item>
                    <NavDropdown.Item>
                        <div style={{textAlign: "center", fontSize: "50%", fontWeight: "bold"}}>
                            Settings
                        </div>
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item onClick={logout}>
                        <div style={{textAlign: "center", fontSize: "50%", fontWeight: "bold"}}>
                            Log out
                        </div>
                    </NavDropdown.Item>
                </NavDropdown>
            );
        } 
        else {
            return (
                <Nav.Link onClick={props.handleLoginShow}>Sign in</Nav.Link>
            );
        }
      }
    
    return (
        <Navbar bg="dark" expand="lg" variant="dark">
            <Navbar.Brand href="/" onClick={() => history.push('/')}>
                CHESS
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />

            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto" />
                <Nav className="mr-sm-2">
                    {renderButton()}
                </Nav>
                
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Navigation;