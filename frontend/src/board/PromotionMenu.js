import React from "react";
import { Dropdown } from "react-bootstrap";

function PromotionMenu(props) {
  return (
    <Dropdown drop="right">
      <Dropdown.Toggle
        variant="secondary"
        id="InGameMenu"
        size="sm"
      ></Dropdown.Toggle>
      <Dropdown.Menu style={{ minWidth: "auto" }}>
        <Dropdown.Item onClick={() => props.setPromotion("Queen")}>
          <div
            style={{ textAlign: "center", fontSize: "50%", fontWeight: "bold" }}
          >
            Queen
          </div>
        </Dropdown.Item>

        <Dropdown.Item onClick={() => props.setPromotion("Bishop")}>
          <div
            style={{ textAlign: "center", fontSize: "50%", fontWeight: "bold" }}
          >
            Bishop
          </div>
        </Dropdown.Item>

        <Dropdown.Item onClick={() => props.setPromotion("Knight")}>
          <div
            style={{ textAlign: "center", fontSize: "50%", fontWeight: "bold" }}
          >
            Knight
          </div>
        </Dropdown.Item>

        <Dropdown.Item onClick={() => props.setPromotion("Rook")}>
          <div
            style={{ textAlign: "center", fontSize: "50%", fontWeight: "bold" }}
          >
            Rook
          </div>
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
}

export default PromotionMenu;
