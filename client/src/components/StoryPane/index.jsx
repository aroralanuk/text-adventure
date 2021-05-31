import React, { useState, useEffect, useRef } from "react";
import Typist from "react-typist";
import "./styles.css";

const StoryPane = ({ choice, story, choiceSelected, restartGame }) => {
  const scrollRef = useRef();
  const [scroll, setScroll] = useState(0);

  // const line = (para) => {
  //   return (
  //     <div>
  //       {text.split("\n").map((i, key) => {
  //         return <div key={key}>{i}</div>;
  //       })}
  //     </div>
  //   );
  // }

  const storyHistory = story.map((para, index) => {
    if (index == story.length - 1) {
      return (
        <p>
          <Typist>{para}</Typist>
        </p>
      );
    } else {
      return <p>{para}</p>;
    }
  });

  // const handleKeyPress = (e) => {
  //   //it triggers by pressing the enter key
  //   console.log(validKeyPress);
  //   if (e.keyCode === 13) {
  //     console.log("works");
  //   }
  // };

  const restartGameButton = (label) => {
    let msg = "";
    if (label == 0) {
      msg =
        "Sadly, you lost this time but you can have another go at surviving the flight. \
      Choose differently and you might just get away scot free. Unless you belief free will is just an illusion \
      and you can never be in control of your destiny.";
    } else {
      msg =
        "Hoorah!!! You won. Savor your sweet victory as you escaped the horrid MH370 and lived to fight another day. But if you're interested about other paths and endings, keep playing. Just remember that curiosity kills the cat.";
    }

    return (
      <div className="game-over-outer">
        <div className="game-over-inner">
          <p>{msg}</p>
          <button
            className="choice-button"
            value={label}
            onClick={restartGame}
            key={label}
          >
            Restart game
          </button>
        </div>
      </div>
    );
  };

  const choiceButtons = choice.map(([label, choice]) => {
    if (label === 0 || label === 1) {
      return restartGameButton(label);
    } else {
      return (
        <button
          className="choice-button"
          onClick={choiceSelected}
          value={choice.title}
          key={label}
        >
          {label}
        </button>
      );
    }
  });

  const scrollAction = () => {
    const scollBottom = scrollRef.current.scrollTop;
    setScroll(scollBottom);
  };

  return (
    <div className="left-section" ref={scrollRef} onScroll={scrollAction}>
      <section className="left-section-content">
        {storyHistory}
        {choiceButtons}
      </section>
    </div>
  );
};

export default StoryPane;
