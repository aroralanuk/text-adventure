import React from "react";
import { Icon } from "semantic-ui-react";

import "./styles.css";
// import { AppBar, Toolbar, Typography, Button } from "@material-ui/core";

export default function NavBar({ updateVisible }) {
  return (
    <div id="navbar">
      <div className="title">
        <h1>The mystery of MH370 - a text adventure</h1>
      </div>
      <Icon name="angle double left" size="big" onClick={updateVisible} />
    </div>
  );
}
