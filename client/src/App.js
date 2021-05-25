import React from "react";
import "./App.css";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
  useParams,
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
          <Route path="/story" component={StoryMode} />
          <Route path="/:id" children={<Child />} />
        </Switch>
      </div>
    </Router>
  );
};

function Child() {
  // We can use the `useParams` hook here to access
  // the dynamic pieces of the URL.
  let { id } = useParams();

  return (
    <div>
      <h3>ID: {id}</h3>
    </div>
  );
}

export default App;
