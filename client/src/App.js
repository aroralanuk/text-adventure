import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from "react-router-dom";
import StoryMode from "./pages/StoryMode";
import HomePage from "./pages/HomePage";

const App = () => {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Redirect from="/" exact to="/home" />
          <Route exact path="/home" component={HomePage} />
          <Route exact path="/story" component={StoryMode} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;
