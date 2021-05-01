import React, { Component } from "react";
import PropTypes from "prop-types";
import Chessboard from "chessboardjsx";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";

class Replay extends Component {
  static propTypes = { children: PropTypes.func };
  constructor(props) {
    super(props);
    this.state = {
      session_id: parseInt(props.session_id),
      fen: "start",
      squareStyles: {},
      history: [],
      step: 0,
      validMoves: [],
      undo: true,
    };
  }

  componentDidMount = () => {
    this.getInfo();
  };

  getInfo = () => {
    fetch("/replay", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        session_id: this.state.session_id,
        step: this.state.step,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        if (json["valid"]) {
          const fen = json["fen"];
          const history = json["history"];
          this.setState({ fen: fen, history: [history] }, () => {
            this.setState(({ validMoves, history }) => ({
              squareStyles: squareStyling({ validMoves, history }),
            }));
          });
        } else {
          this.setState({ step: this.state.step - 1 });
        }
      });
  };

  triggerEffect = (val) => {
    let tmp = this.state.step + val;
    if (tmp < 0) tmp = 0;
    if (tmp !== this.state.step) {
      this.setState({ step: tmp }, () => {this.getInfo();});
    }
  };

  render() {
    const { fen, squareStyles, undo } = this.state;

    return this.props.children({
      squareStyles,
      position: fen,
      undo,
      triggerEffect: this.triggerEffect,
    });
  }
}

export default function Replays(props) {
  return (
    <div>
      <Replay session_id={props.match.params.session_id}>
        {({ position, undo, squareStyles, triggerEffect }) => (
          <Container fluid style={{ width: "100vw" }}>
            <Row className="justify-content-center mt-3">
              <Chessboard
                id="ChessBoard"
                width={350}
                position={position}
                boardStyle={{
                  borderRadius: "5px",
                  boxShadow: `0 5px 15px rgba(0, 0, 0, 0.5)`,
                }}
                squareStyles={squareStyles}
                draggable={false}
                undo={undo}
              />
            </Row>
            <Row className="justify-content-center mt-3">
              <Button
                variant="outline-dark"
                className="ml-2"
                onClick={() => triggerEffect(-1)}
              >
                {" "}
                {"<"}{" "}
              </Button>
              <Button
                variant="outline-dark"
                className="ml-2"
                onClick={() => triggerEffect(1)}
              >
                {" "}
                {">"}{" "}
              </Button>
            </Row>
          </Container>
        )}
      </Replay>
    </div>
  );
}

const squareStyling = ({ validMoves, history }) => {
  const sourceSquare = history.length && history[history.length - 1].src;
  var srcStyle = "rgba(255, 255, 0, 0.4)";
  if (validMoves.includes(sourceSquare)) {
    srcStyle =
      "radial-gradient(circle, #0d8230 36%, transparent 40%), rgba(255, 255, 0, 0.4)";
  }

  const targetSquare = history.length && history[history.length - 1].tar;
  var tarStyle = "rgba(255, 255, 0, 0.4)";
  if (validMoves.includes(targetSquare)) {
    tarStyle =
      "radial-gradient(circle, #0d8230 36%, transparent 40%), rgba(240, 255, 0, 0.4)";
  }

  return {
    ...(history.length && {
      [sourceSquare]: {
        background: srcStyle,
      },
    }),
    ...(history.length && {
      [targetSquare]: {
        background: tarStyle,
      },
    }),
  };
};
