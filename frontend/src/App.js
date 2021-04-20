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


  
  return (
    <Container fluid style={{ paddingLeft: 0, paddingRight: 0 }}>
      <Router>
        <Navigation handleLoginShow={handleLoginShow}/>
        <Login showLogin={showLogin} handleLoginClose={handleLoginClose} handleSignupShow={handleSignupShow}/>
        <Signup showSignup={showSignup} handleSignupClose={handleSignupClose} />
        <Switch>
          <Route path="/chess/:session_id" exact component={WithMoveValidation} />
          <Route path="/" exact>
            <Menu />
          </Route>
        </Switch>
      </Router>
    </Container>
  );
}

export default App;



