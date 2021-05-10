import React from "react";
import { Dropdown } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

function InGameMenu() {
  const history = useHistory();

  return (
    <Dropdown>
      <Dropdown.Toggle variant="secondary" id="InGameMenu" size="sm">
        MENU
      </Dropdown.Toggle>
      <Dropdown.Menu style={{ minWidth: "auto" }}>
        <Dropdown.Item onClick={() => history.push("/")}>
          <div
            style={{ textAlign: "center", fontSize: "50%", fontWeight: "bold" }}
          >
            QUIT
          </div>
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default InGameMenu;
