import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import NavBar from "../components/NavBar/index";
import StoryPane from "../components/StoryPane/index";
import AIPane from "../components/AIPane/index";
import API from "../API";

const StoryMode = () => {
  const [story, setStory] = useState([]);
  const [choice, setChoice] = useState([]);
  const [status, setStatus] = useState(false);
  const [currentHint, setCurrentHint] = useState("No hints here");
  const history = useHistory();
  const game_id = history.location.state.game_id;

  useEffect(() => {
    API.getGameUpdate(game_id).then((response) => {
      const { choices, story_so_far, hint } = response.data;
      setStory(story_so_far);
      setChoice(choices);
      setCurrentHint(hint[0]);
      console.log(hint);
    });
  }, [status]);

  const choiceSelected = async (e) => {
    e.preventDefault();
    let body = { choice_made: e.target.value };
    API.updateGame(game_id, body).then((response) => {
      if (response.status === 200) {
        setStatus(status + 1);
      }
    });
  };

  const restartGame = async (e) => {
    e.preventDefault();
    API.createGame().then((response) => {
      const game_id = response.data.game_id;
      history.push({
        pathname: "/story/" + game_id,
        state: { game_id: game_id },
      });
      if (response.status === 200) {
        setStatus(status + 1);
      }
    });
  };

  return (
    <div className="main-page">
      <NavBar />
      <section className="main-section">
        <StoryPane
          story={story}
          choice={choice}
          choiceSelected={choiceSelected}
          restartGame={restartGame}
        />
        <AIPane hint={currentHint} />
      </section>
    </div>
  );
};

export default StoryMode;
