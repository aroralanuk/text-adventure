import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import { Header, Icon, Menu, Segment, Sidebar } from "semantic-ui-react";

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
  const [currTrust, setCurrTrust] = useState(0);

  // setting mood as variable as it wasn't updating as a state and then assigning it
  const [moody, setMoody] = useState(33);
  let diffMood = moody;

  const [visible, setVisible] = useState(false);
  const [newGame, setNewGame] = useState(true);
  const [hintTaken, setHintTaken] = useState(false);

  const history = useHistory();
  const game_id = history.location.state.game_id;

  useEffect(() => {
    // sending a GET request to the API
    API.getGameUpdate(game_id).then((response) => {
      const { choices, story_so_far, hint, survival_chance, trust, mood } =
        response.data;
      setStory(story_so_far);
      setChoice(choices);
      setCurrentHint(hint);

      setNewGame(false);

      // checking if valid survival, trust and mood values
      if (survival_chance >= 0 && survival_chance <= 1.1)
        setSurvival(Math.round(survival_chance * 100));
      if (trust >= 0 && trust <= 1.1) setCurrTrust(Math.round(trust * 100));
      if (mood >= 0 && mood <= 1.1) {
        diffMood = Math.round(mood * 100);
        setMoody(diffMood);
      }
      setHintTaken(false);
    });
  }, [status, visible]);

  const choiceSelected = async (e) => {
    e.preventDefault();

    // default value if no hint available
    let hintAgreedWith = false;
    let hintTitle = "no_hint";
    let body = { choice_made: e.target.value };

    // getting hint title if a hint is provided
    if (typeof currentHint == "object" && currentHint.choice) {
      hintTitle = currentHint.choice;
    }

    // checking if the user agreed with the hint
    if (hintTaken && e.target.value === hintTitle) {
      delightGhost();
    } else if (hintTaken) {
      upsetGhost();
    }

    // console.log(diffMood);
    // body with additional hint info

    body["hint_taken"] = hintTaken;
    body["hint_agreed_with"] = hintAgreedWith;
    body["mood"] = diffMood / 100;

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

  // if disagree with hint
  const upsetGhost = () => {
    if (diffMood >= 70) {
      diffMood = 100;
    } else {
      diffMood = diffMood + 30;
    }
  };

  // if agree with hint
  const delightGhost = () => {
    if (diffMood <= 30) {
      diffMood = 0;
    } else {
      diffMood = diffMood - 30;
    }
  };

  const updateVisible = () => {
    setVisible(!visible);
  };

  return (
    <Sidebar.Pushable as={Segment} style={{ border: "0px" }}>
      <Sidebar.Pusher dimmed={visible}>
        <Segment
          basic
          className="main-page"
          style={{ backgroundColor: "black" }}
        >
          <NavBar updateVisible={updateVisible} />
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
              trust={currTrust}
              mood={moody}
            />
          </section>
        </Segment>
      </Sidebar.Pusher>

      {/* sidebar component for the 'About us' */}
      {/* TODO: push it to a separate file */}
      <Sidebar
        as={Menu}
        animation="overlay"
        icon="labeled"
        inverted
        direction="right"
        onHide={() => setVisible(false)}
        vertical
        visible={visible}
        width="thin"
        style={{ width: "30vw" }}
      >
        <Menu.Item as="a" style={{ margin: "2rem" }}>
          <Header
            as="h3"
            style={{ color: "white", margin: "1.5rem", fontSize: "2rem" }}
          >
            About this project
          </Header>
          <Header.Subheader
            style={{ color: "#aaa", fontSize: "1.2rem", lineHeight: "1.5rem" }}
          >
            We made this AI-guided text-adventure game as our final project for{" "}
            <a
              href="https://kristenvaccaro.github.io/human-ai/"
              style={{ color: "#3f0" }}
            >
              CSE 190{" "}
            </a>
            at UC San Diego focusing on recommender systems, transparency, and
            explainability in the context of human-AI interactions. More details
            can be found in the{" "}
            <a
              href="https://github.com/aroralanuk/text-adventure"
              style={{ color: "#3f0" }}
            >
              github repo.
            </a>
          </Header.Subheader>
          <br /> <br /> <br />
        </Menu.Item>
        <Menu.Item as="a" style={{ margin: "2rem" }}>
          <Header
            as="h3"
            style={{ color: "white", margin: "1.5rem", fontSize: "2rem" }}
          >
            About us
          </Header>
          <Header.Subheader
            style={{
              color: "#aaa",
              fontSize: "1.2rem",
              lineHeight: "1.5rem",
            }}
          >
            Find us on these platforms:
            <br /> <br />
            Kunal Arora{"  "}
            <a
              href="https://github.com/aroralanuk"
              style={{ color: "#3f0", marginLeft: "0.5rem" }}
            >
              <Icon name="github" />
            </a>
            <a
              href="mailto:crazentonkunalizar@gmail.com"
              style={{ color: "#3f0" }}
            >
              <Icon name="mail" />
            </a>
            <a href="https://twitter.com/arorAlanuK" style={{ color: "#3f0" }}>
              <Icon name="twitter" />
            </a>
            <br />
            McKinley Souder
            <a
              href="https://github.com/mckinleysouder"
              style={{ color: "#3f0", marginLeft: "0.5rem" }}
            >
              <Icon name="github" />
            </a>
            <a href="mailto:msouder@ucsd.edu" style={{ color: "#3f0" }}>
              <Icon name="mail" />
            </a>
            <br />
            Faith DiSandro
            <a
              href="https://github.com/faith0disandro"
              style={{ color: "#3f0", marginLeft: "0.5rem" }}
            >
              <Icon name="github" />
            </a>
            <a href="mailto:fdisandr@ucsd.edu" style={{ color: "#3f0" }}>
              <Icon name="mail" />
            </a>
            <br />
          </Header.Subheader>
          <br /> <br /> <br />
        </Menu.Item>
      </Sidebar>
    </Sidebar.Pushable>
  );
};

export default StoryMode;
