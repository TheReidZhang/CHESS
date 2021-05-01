import React, { Component } from "react";
import PropTypes from "prop-types";
import Chessboard from "chessboardjsx";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import "bootstrap/dist/css/bootstrap.min.css";
import Info from "./Info";
import PromotionMenu from "./PromotionMenu";
import GameOption from "./GameOption";
import { useParams, withRouter } from "react-router-dom";

class ChessBoard extends Component {
  static propTypes = {
    children: PropTypes.func,
    history: PropTypes.object.isRequired,
  };

  constructor(props) {
    super(props);
    this.state = {
      session_id: parseInt(props.session_id),
      fen: "start",
      // custom square styles
      squareStyles: {},
      // square with the currently clicked piece
      pieceSquare: "",
      // currently clicked square
      square: "",
      // array of past game moves
      history: [],
      validMoves: [],
      turn: "Loading...",
      status: "Loading...",
      role: "Queen",
      undo: true,
      mode: "Loading...",
    };
  }

  componentDidMount = () => {
    this.getInfo();
  };

  getInfo = () => {
    fetch("/chess/info", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        session_id: this.state.session_id,
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        if (json["valid"]) {
          const fen = json["fen"];
          const status = json["status"];
          const turn = json["turn"];
          const history = json["history"];
          const mode = json["mode"];
          this.setState(
            {
              fen: fen,
              status: status,
              turn: turn,
              history: history,
              mode: mode,
            },
            () => {
              this.setState(({ validMoves, history }) => ({
                squareStyles: squareStyling({ validMoves, history }),
              }));
            }
          );
        } else {
          alert("Log in first or this session does not belong to you!");
          const { history } = this.props;
          history.push("/");
        }
      });
  };

  // show possible moves
  highlightSquare = (sourceSquare, squaresToHighlight) => {
    const highlightStyles = [sourceSquare, ...squaresToHighlight].reduce(
      (a, c) => {
        return {
          ...a,
          ...{
            [c]: {
              background:
                "radial-gradient(circle, #0d8230 36%, transparent 40%)",
              borderRadius: "50%",
            },
          },
          ...squareStyling({
            validMoves: this.state.validMoves,
            history: this.state.history,
          }),
        };
      },
      {}
    );

    this.setState(({ squareStyles }) => ({
      squareStyles: { ...squareStyles, ...highlightStyles },
    }));
  };

  takeback = () => {
    let ed = 0;
    if (this.state.mode !== "pvp") {
      ed = 1;
    }
    for (var i = 0; i <= ed; i++) {
      fetch("/undo", {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({
          session_id: this.state.session_id,
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          this.getInfo();
        });
    }
  };

  setPromotion = (role) => {
    this.setState({ role: role });
  };

  onSquareClick = (square) => {
    // Clicked some piece
    if (this.state.pieceSquare !== "") {
      fetch("/chess/update", {
        headers: { "Content-Type": "application/json" },
        method: "POST",
        body: JSON.stringify({
          src: this.state.pieceSquare,
          tar: square,
          session_id: this.state.session_id,
          role: this.state.role,
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          if (json["valid"]) {
            fetch("/chess/info", {
              headers: { "Content-Type": "application/json" },
              method: "POST",
              body: JSON.stringify({
                session_id: this.state.session_id,
              }),
            })
              .then((response) => response.json())
              .then((json) => {
                if (json["valid"]) {
                  const fen = json["fen"];
                  const status = json["status"];
                  const turn = json["turn"];
                  const history = json["history"];
                  this.setState({
                    fen: fen,
                    pieceSquare: "",
                    status: status,
                    turn: turn,
                    history: history,
                    validMoves: [],
                  });
                } else {
                  alert("Log in first or this session does not belong to you!");
                  const { history } = this.props;
                  history.push("/");
                }

                this.setState(({ validMoves, history }) => ({
                  squareStyles: squareStyling({ validMoves, history }),
                }));
              });
            const update_is_being_checked = json["is_being_checked"];
            if (update_is_being_checked) {
              setTimeout(function () {
                alert("check!");
              }, 0);
            }
            const update_game_status = json["game_status"];
            if (update_game_status !== "Continue") {
              setTimeout(function () {
                alert(update_game_status);
              }, 0);
            }

            return;
          }
        });
    }

    this.setState(({ validMoves, history }) => ({
      squareStyles: squareStyling({ validMoves, history }),
    }));
    fetch("/chess/" + this.state.session_id + "/" + square)
      .then((response) => response.json())
      .then((json) => {
        const moves = json["moves"];
        const squaresToHighlight = [];
        for (var i = 0; i < moves.length; i++) {
          squaresToHighlight.push(moves[i]);
        }
        this.setState({ pieceSquare: square, validMoves: squaresToHighlight });
        this.highlightSquare(square, squaresToHighlight);
      });
  };

  render() {
    const { fen, squareStyles, turn, status, undo, mode } = this.state;

    return this.props.children({
      turn,
      status,
      squareStyles,
      position: fen,
      undo,
      mode,
      onSquareClick: this.onSquareClick,
      setPromotion: this.setPromotion,
      takeback: this.takeback,
    });
  }
}

ChessBoard = withRouter(ChessBoard);

export default function WithMoveValidation(props) {
  let { session_id } = useParams();
  return (
    <div>
      <ChessBoard session_id={session_id}>
        {({
          turn,
          status,
          position,
          undo,
          mode,
          squareStyles,
          onSquareClick,
          setPromotion,
          takeback,
        }) => (
          <Container fluid style={{ width: "100vw" }}>
            <Row>
              <div className="mr-auto">
                <Info turn={turn} status={status} mode={mode} />
              </div>
              <div className="mr-sm-2 mt-1">
                <GameOption takeback={takeback} />
              </div>
            </Row>
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
                onSquareClick={onSquareClick}
                draggable={false}
                undo={undo}
              />
              <PromotionMenu setPromotion={setPromotion} />
            </Row>
          </Container>
        )}
      </ChessBoard>
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
