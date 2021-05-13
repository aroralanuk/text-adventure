import React from "react";
import { Typography } from "@material-ui/core";
import logo from "../images/plane_ascii.png";
import "./styles.css";

export default function HomePage() {
  return (
    <div className="main-page">
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          transform: "translate(-50%, -50%)",
        }}
        className="home-section"
      >
        <img src={logo} width="100%" alt="plane ascii art" />
        <Typography align="center" id="welcome-text">
          Welcome to 'THE MYSTERY OF MH370 - A TEXT ADVENTURE' game where you
          choose your own destiny after boarding the infamous flight MH370. Your
          mission, should you choose to accept it, is to survive the survive the
          flight and land in Shanghai in one piece. You'll be have an AI
          assistant guide you along the way. Press the button below to start
          your misadventure ;)
        </Typography>
        <button id="start-button">
          <a href="/story">Start a new game</a>
        </button>
      </div>
    </div>
  );
}
