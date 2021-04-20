import './App.css';
import Navigation from './page/navbar'
import Login from './page/login'
import Signup from './page/signup'
import React, { useState } from 'react';
import WithMoveValidation from "./board/WithMoveValidation";
import Menu from './menu/menu';
import Container from 'react-bootstrap/Container'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const handleLoginClose = () => setShowLogin(false);
  const handleLoginShow = () => setShowLogin(true);

  const [showSignup, setShowSignup] = useState(false);
  const handleSignupClose = () => setShowSignup(false);
  const handleSignupShow = () => setShowSignup(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  const renderMenu = () => {
    if (isLoggedIn) {
      return <Menu />
    }
    else {
      return (
      <div>
        <div style={{textAlign: "left", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          Every chess master was once a beginner.
        </div>
        <div style={{textAlign: "right", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          – Irving Chernev
        </div>

        <br/>
        <br/>

        <div style={{textAlign: "left", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          I have come to the personal conclusion that while all artists are not chess players, all chess players are artists.
        </div>
        <div style={{textAlign: "right", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          – Marcel Duchamp
        </div>
        
        <br/>
        <br/>
        
        <div style={{textAlign: "left", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          Avoid the crowd. Do your own thinking independently. Be the chess player, not the chess piece.
        </div>
        <div style={{textAlign: "right", fontFamily: 'Original Surfer', fontSize:"150%"}}>
          – Ralph Charell
        </div>

        
      </div>
      )
    }
  }
  
  return (
    <Container fluid style={{ paddingLeft: 0, paddingRight: 0 }}>
      <Router>
        <Navigation handleLoginShow={handleLoginShow} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
        <Login showLogin={showLogin} handleLoginClose={handleLoginClose} handleSignupShow={handleSignupShow}/>
        <Signup showSignup={showSignup} handleSignupClose={handleSignupClose} />
        <Switch>
          <Route path="/chess/:session_id" exact component={WithMoveValidation} />
          <Route path="/" exact>
            <div className="center-container">
              {renderMenu()}
            </div>
          </Route>
        </Switch>
      </Router>
    </Container>
  );
}

export default App;



