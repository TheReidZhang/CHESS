import React, { useState, useEffect } from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import "bootstrap/dist/css/bootstrap.min.css";
import { useHistory } from "react-router-dom";

function Navigation(props) {
  const [userName, setUserName] = useState("");
  const [totalHours, setTotalHours] = useState(0);
  const [score, setScore] = useState(0);

  useEffect(() => {
    fetch("/user")
      .then((response) => response.json())
      .then((json) => {
        if (json["valid"]) {
          props.setIsLoggedIn(true);
          setUserName(json["username"]);
          setTotalHours(json["total_hours"]);
          setScore(json["score"]);
        }
      });
  }, []);

  const history = useHistory();
  const logout = () => {
    fetch("/logout")
      .then((response) => response.json())
      .then((json) => {
        alert(json["msg"]);
        history.push("/");
        history.go(0);
      });
  };

  const renderButton = () => {
    if (props.isLoggedIn) {
      return (
        <NavDropdown
          title={userName}
          alignRight
          id="basic-nav-dropdown"
          style={{ minWidth: "auto" }}
        >
          <NavDropdown.Item>
            <div
              style={{
                textAlign: "center",
                fontSize: "50%",
                fontWeight: "bold",
              }}
            >
              Total Hours: {totalHours}
            </div>
          </NavDropdown.Item>
          <NavDropdown.Item>
            <div
              style={{
                textAlign: "center",
                fontSize: "50%",
                fontWeight: "bold",
              }}
            >
              Score: {score}
            </div>
          </NavDropdown.Item>
          <NavDropdown.Divider />
          <NavDropdown.Item>
            <div
              style={{
                textAlign: "center",
                fontSize: "50%",
                fontWeight: "bold",
              }}
            >
              Profile
            </div>
          </NavDropdown.Item>
          <NavDropdown.Item>
            <div
              style={{
                textAlign: "center",
                fontSize: "50%",
                fontWeight: "bold",
              }}
            >
              Settings
            </div>
          </NavDropdown.Item>
          <NavDropdown.Divider />
          <NavDropdown.Item onClick={logout}>
            <div
              style={{
                textAlign: "center",
                fontSize: "50%",
                fontWeight: "bold",
              }}
            >
              Log out
            </div>
          </NavDropdown.Item>
        </NavDropdown>
      );
    } else {
      return <Nav.Link onClick={props.handleLoginShow}>Sign in</Nav.Link>;
    }
  };

  return (
    <Navbar bg="dark" expand="lg" variant="dark">
      <Navbar.Brand href="/" onClick={() => history.push("/")}>
        <div style={{ fontFamily: "Zen Dots" }}>CHESS</div>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />

      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto" />
        <Nav className="mr-sm-2">{renderButton()}</Nav>
        <Nav className="mr-sm-2">{props.boopButton}</Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Navigation;
