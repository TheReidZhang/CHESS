import "./App.css";
import Navigation from "./menu/Navigation";
import Login from "./menu/Login";
import Signup from "./menu/Signup";
import React, { useState } from "react";
import WithMoveValidation from "./board/WithMoveValidation";
import MainMenu from "./menu/MainMenu";
import Container from "react-bootstrap/Container";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Replays from "./board/Replay";
import useSound from "use-sound";
import boopSfx from "./BodyFunk.mp3";

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const handleLoginClose = () => setShowLogin(false);
  const handleLoginShow = () => setShowLogin(true);
  const [showSignup, setShowSignup] = useState(false);
  const handleSignupClose = () => setShowSignup(false);
  const handleSignupShow = () => setShowSignup(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  let audio = new Audio("/move.wav");

  const BoopButton = () => {
    const [play, { stop, isPlaying }] = useSound(boopSfx, { volume: 0.2 });
    return (
      <button
        onClick={() => {
          isPlaying ? stop() : play();
        }}
      >
        <span role="img" aria-label="trumpet">
          🎺
        </span>
      </button>
    );
  };

  const renderMenu = () => {
    if (isLoggedIn) {
      return <MainMenu />;
    } else {
      return (
        <div>
          <div
            style={{
              textAlign: "left",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            Every chess master was once a beginner.
          </div>
          <div
            style={{
              textAlign: "right",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            – Irving Chernev
          </div>

          <br />
          <br />

          <div
            style={{
              textAlign: "left",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            I have come to the personal conclusion that while all artists are
            not chess players, all chess players are artists.
          </div>
          <div
            style={{
              textAlign: "right",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            – Marcel Duchamp
          </div>

          <br />
          <br />

          <div
            style={{
              textAlign: "left",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            Avoid the crowd. Do your own thinking independently. Be the chess
            player, not the chess piece.
          </div>
          <div
            style={{
              textAlign: "right",
              fontFamily: "Original Surfer",
              fontSize: "150%",
            }}
          >
            – Ralph Charell
          </div>
        </div>
      );
    }
  };

  return (
    <Container fluid style={{ paddingLeft: 0, paddingRight: 0 }}>
      <Router>
        <Navigation
          handleLoginShow={handleLoginShow}
          isLoggedIn={isLoggedIn}
          setIsLoggedIn={setIsLoggedIn}
          boopButton={BoopButton()}
        />
        <Login
          showLogin={showLogin}
          handleLoginClose={handleLoginClose}
          handleSignupShow={handleSignupShow}
        />
        <Signup showSignup={showSignup} handleSignupClose={handleSignupClose} />
        <Switch>
          <Route path="/chess/:session_id">
            <WithMoveValidation audio={audio} />
          </Route>
          <Route path="/replay/:session_id">
            <Replays audio={audio} />
          </Route>
          <Route path="/" exact>
            <div className="center-container">{renderMenu()}</div>
          </Route>
        </Switch>
      </Router>
    </Container>
  );
}

export default App;
