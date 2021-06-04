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
  const [currentHint, setCurrentHint] = useState("no_hint_api");
  const [survival, setSurvival] = useState(0);
  const [newGame, setNewGame] = useState(true);
  const [hintTaken, setHintTaken] = useState(false);

  const history = useHistory();
  const game_id = history.location.state.game_id;

  useEffect(() => {
    API.getGameUpdate(game_id).then((response) => {
      const { choices, story_so_far, hint, survival_chance } = response.data;
      setStory(story_so_far);
      setChoice(choices);
      setCurrentHint(hint);
      setNewGame(false);
      if (survival_chance >= 0 && survival_chance <= 1.1)
        setSurvival(Math.round(survival_chance * 100));
      setHintTaken(false);
      // console.log(survival_chance);
    });
  }, [status]);

  const choiceSelected = async (e) => {
    e.preventDefault();

    // default value if no hint available
    let hintAgreedWith = false;
    let hintTitle = "no_hint";

    // getting hint title if a hint is provided
    if (currentHint.length && typeof currentHint[1] == "object") {
      hintTitle = currentHint[1].title;
    }

    // checking if the user agreed with the hint
    if (hintTaken && e.target.value === hintTitle) {
      hintAgreedWith = true;
    }

    // body with additional hint info
    let body = { choice_made: e.target.value };
    body["hint_taken"] = hintTaken;
    body["hint_agreed_with"] = hintAgreedWith;

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
        setNewGame(true);
      }
    });
  };

  const updateHintTaken = async (e) => {
    setHintTaken(true);
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
        <AIPane
          hint={currentHint}
          restarted={newGame}
          currSurvival={survival}
          hintTaken={updateHintTaken}
        />
      </section>
    </div>
  );
};

export default StoryMode;
