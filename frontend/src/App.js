import './App.css';
import React from 'react';
import WithMoveValidation from "./board/WithMoveValidation";
import Menu from './menu/menu';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Switch>
      <Route path="/chess/:session_id" exact component={WithMoveValidation} />

        <Route path="/" exact>
          <Menu />
        </Route>
      </Switch>
    </Router>
   
  );
}

export default App;



