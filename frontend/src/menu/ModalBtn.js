import React from "react";
import { useHistory } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import "bootstrap/dist/css/bootstrap.min.css";

function ModalBtn(props) {
  const history = useHistory();

  return (
    <Row className="align-items-center mb-3">
      <Col>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Button
            variant="outline-dark"
            size="sm"
            onClick={() => history.push("/chess/" + props.session_id)}
          >
            Mode: {props.mode.toUpperCase()}
            <br />
            Session ID: {props.session_id}
            <br />
            Start Time: {props.start_time}
            <br />
            Last Update: {props.last_update}
            <br />
          </Button>
        </div>
      </Col>
    </Row>
  );
}

export default ModalBtn;
