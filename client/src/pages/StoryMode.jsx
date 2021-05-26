import { Grid } from "@material-ui/core";
import React from "react";
import NavBar from "../components/NavBar/index";
import StoryPane from "../components/StoryPane/index";
import AIPane from "../components/AIPane/index";

export default function StoryMode() {
  return (
    <div className="main-page">
      <NavBar />
      <section className="main-section">
        <StoryPane />
        <AIPane />
      </section>
    </div>
  );
}
