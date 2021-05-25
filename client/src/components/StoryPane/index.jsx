import React, { useState, useRef } from "react";
import "./styles.css";

const StoryPane = ({ choice, story, choiceSelected, restartGame }) => {
  const scrollRef = useRef();
  const [scroll, setScroll] = useState(0);
  // if (choice)
  // const dead_or_alive = choice[0][0];

  const storyHistory = story.map((para) => {
    return <p>{para}</p>;
  });

  const restartGameButton = (label) => {
    return (
      <button className="choice-button" value={label} onClick={restartGame}>
        Restart game
      </button>
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
