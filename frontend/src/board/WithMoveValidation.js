import React, { Component } from "react";
import PropTypes from "prop-types";
import Chessboard from "chessboardjsx";
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css';
import Info from './Info';
import PromotionMenu from "./PromotionMenu";
import GameOption from "./GameOption"


class ChessBoard extends Component {
  static propTypes = { children: PropTypes.func };

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
      role: "Queen"
    };
  }

  async componentDidMount() {
    const fen_response = await fetch('/chess/info', {
      method: 'POST',
      body: JSON.stringify({
      session_id: this.state.session_id})
    });
    
    if (!fen_response.ok) {
      throw Error("None-existed session.");
    }
    
    const fen_json = await fen_response.json();
    const fen = fen_json["fen"];
    const status = fen_json["status"];
    const turn = fen_json["turn"]
    const history = fen_json["history"];
    const promotion = fen_json["promotion"];
    this.setState({fen: fen, status: status, turn: turn, history: history, promotion: promotion});
    this.setState(({ validMoves, history }) => ({
      squareStyles: squareStyling({ validMoves, history })
    }));
  }

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
              borderRadius: "50%"
            }
          },
          ...squareStyling({
            validMoves: this.state.validMoves,
            history: this.state.history
          })
        };
      },
      {}
    );

    this.setState(({ squareStyles }) => ({
      squareStyles: { ...squareStyles, ...highlightStyles }
    }));
  };

  takeback = async() => {
    const response = await fetch('/undo', {
      method: 'POST',
      body: JSON.stringify({ 
        session_id: this.state.session_id,
       })
    });
    const json = response.json();
    if (json["valid"]) {
      this.setState({
        fen: json["fen"],
        pieceSquare: "",
        status: json["status"],
        turn: json["turn"],
        history: json["history"],
        validMoves: []
    });
    }
  } 

  setPromotion = (role) => {
    this.setState({role: role})
    
  }


  onSquareClick = async (square) => {
    // Clicked some piece
    if (this.state.pieceSquare !== "") {
      const update_response = await fetch('/chess/update', {
        method: 'POST',
        body: JSON.stringify({ 
          src: this.state.pieceSquare,
          tar: square,
          session_id: this.state.session_id,
          role: this.state.role
         })
      });
      const update_json = await update_response.json();
      const update_valid = update_json["valid"];

      if (update_valid) {   
        const fen_response = await fetch('/chess/info', {
          method: 'POST',
          body: JSON.stringify({
          session_id: this.state.session_id})
        });
        const fen_json = await fen_response.json();
        const fen = fen_json["fen"];
        const status = fen_json["status"];
        const turn = fen_json["turn"];
        const history = fen_json["history"];
        const promotion = fen_json["promotion"];
        this.setState({
          fen: fen,
          pieceSquare: "",
          status: status,
          turn: turn,
          history: history,
          validMoves: [],
          promotion: promotion
        });
        

        this.setState(({ validMoves, history }) => ({
          squareStyles: squareStyling({ validMoves, history })
        }));

        if (promotion) {
          
        }
        
        const update_is_being_checked = update_json["is_being_checked"];
        if (update_is_being_checked) {
          setTimeout(function() {
            alert('check!');
           }, 0);
        }
        const update_game_status = update_json["game_status"];
        if (update_game_status !== "Continue") {
          setTimeout(function() {
            alert(update_game_status);
           }, 0);
        }
        
         
        return;
      }
    
    }
    
    this.setState(({ validMoves, history }) => ({
      squareStyles: squareStyling({ validMoves, history })
    }));
    const response = await fetch('/chess/' + this.state.session_id + '/'+square);
    const json = await response.json();
    const moves = json["moves"];
    const squaresToHighlight = [];
    for (var i = 0; i < moves.length; i++) {
      squaresToHighlight.push(moves[i]);
    }
    this.setState({pieceSquare: square, validMoves: squaresToHighlight});
    this.highlightSquare(square, squaresToHighlight);
  };

  render() {
    const { fen, squareStyles, turn, status, promotion } = this.state;
    
    return this.props.children({
      turn,
      status,
      promotion,
      squareStyles,
      position: fen,
      onSquareClick: this.onSquareClick,
      setPromotion: this.setPromotion,
      takeback: this.takeback
    });
  }
}

export default function WithMoveValidation(props) {

  return (
    <div>
      <ChessBoard session_id={props.match.params.session_id}>
        {({        
          turn,
          status,
          promotion,
          position, 
          squareStyles,
          onSquareClick,
          setPromotion,
          takeback
        }) => (
          <Container fluid style={{width:"100vw"}}>
            <Row>
              <div className="mr-auto">
                <Info turn={turn} status={status}/>
                </div>
                <div className="mr-sm-2 mt-1">
                <GameOption takeback={takeback}/>
                </div>
            </Row>
            <Row className="justify-content-center mt-3"> 
            <Chessboard
              id="ChessBoard"
              width={350}
              position={position}
              boardStyle={{
                borderRadius: "5px",
                boxShadow: `0 5px 15px rgba(0, 0, 0, 0.5)`
              }}
              squareStyles={squareStyles}
              onSquareClick={onSquareClick}
              draggable={false}
            />
            <PromotionMenu show={promotion} setPromotion={setPromotion}/>
            </Row>
          </Container>
        )}
      </ChessBoard>
    </div>
  );
}

const squareStyling = ({ validMoves, history }) => {
  const sourceSquare = history.length && history[history.length - 1].src;
  var srcStyle = "rgba(255, 255, 0, 0.4)"
  if (validMoves.includes(sourceSquare)) {srcStyle = "radial-gradient(circle, #0d8230 36%, transparent 40%), rgba(255, 255, 0, 0.4)"} 
  
  const targetSquare = history.length && history[history.length - 1].tar;
  var tarStyle = "rgba(255, 255, 0, 0.4)"
  if (validMoves.includes(targetSquare)) {tarStyle = "radial-gradient(circle, #0d8230 36%, transparent 40%), rgba(240, 255, 0, 0.4)"} 

  return {
    ...(history.length && {
      [sourceSquare]: {
        background: srcStyle
      }
    }),
    ...(history.length && {
      [targetSquare]: {
        background: tarStyle
      }
    })
  };
};
