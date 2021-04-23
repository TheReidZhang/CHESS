import React, { Component } from "react";
import PropTypes from "prop-types";
import Chessboard from "chessboardjsx";
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button'



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
      undo: true
    };
  }
 
  componentDidMount = async () => {
    await this.getInfo();
  }

  getInfo = async() => {
    const fen_response = await fetch('/replay', {
      method: 'POST',
      body: JSON.stringify({
      session_id: this.state.session_id, step: this.state.step})
    });
    if (!fen_response.ok) {
      throw Error("None-existed session.");
    }
    const fen_json = await fen_response.json();
    if (fen_json["valid"]) {
    const fen = fen_json["fen"];
    const history = fen_json["history"];
    this.setState({fen: fen, history: [history]}, () => {
      this.setState(({ validMoves, history }) => ({
        squareStyles: squareStyling({ validMoves, history })
      }));
    });
    }
    else {
        this.setState({ step: this.state.step - 1})
    }
  }

  triggerEffect = async(val) => {
    let tmp = this.state.step + val;
    if (tmp < 0) tmp = 0;
    const fen_response = await fetch('/replay', {
      method: 'POST',
      body: JSON.stringify({
      session_id: this.state.session_id, step: tmp})
    });
    if (!fen_response.ok) {
      throw Error("None-existed session.");
    }
    const fen_json = await fen_response.json();
    if (fen_json["valid"]) {
    const fen = fen_json["fen"];
    const history = fen_json["history"];
    this.setState({fen: fen, history: [history]}, () => {
      this.setState(({ validMoves, history }) => ({
        squareStyles: squareStyling({ validMoves, history })
      }));
    });
    this.setState({step: tmp})
    }
    else {
        this.setState({ step: this.state.step - 1})
    }
  }

  takeback = async() => {
    const response = await fetch('/undo', {
      method: 'POST',
      body: JSON.stringify({ 
        session_id: this.state.session_id
       })
    });
    const json = await response.json();
    if (json["valid"]) {
      this.setState({undo: true});
    }
}

  render() {
    const { fen, squareStyles, undo} = this.state;
    
    return this.props.children({
      squareStyles,
      position: fen,
      undo,
      triggerEffect: this.triggerEffect
    });
  }
}

export default function Replays(props) {

  return (
    <div>
      <Replay session_id={props.match.params.session_id}>
        {({        
          position, 
          undo,
          squareStyles,
          triggerEffect
        }) => (
          <Container fluid style={{width:"100vw"}}>
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
              draggable={false}
              undo={undo}
            />
            </Row>
            <Row className="justify-content-center mt-3"> 
            <Button variant="outline-dark" className="ml-2" onClick={() => triggerEffect(-1)}> {"<"} </Button>
            <Button variant="outline-dark" className="ml-2" onClick={() => triggerEffect(1)}> {">"} </Button>
            </Row>
        </Container>
        )}
      </Replay>
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
