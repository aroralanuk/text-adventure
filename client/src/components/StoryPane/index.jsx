import React, { useState, useRef } from "react";
import "./styles.css";

export default function StoryPane() {
  const [storyline, setStoryline] = useState([
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],

    [
      "You're Huang, a Chinese exchange student on the last day of your stay in Singapore.",
    ],
    ["> beep beep beep..."],
  ]);
  const [choices, setChoices] = useState([
    [
      "Walk into the cockpit",
      {
        desc: '"Rescue me from this insane guy. He\'s planning to put in a nose dive and kill all these people." pleads the first officer who was held by his neck by the captain who now threatens you, "Stay away from this, kid. I just want to go home."\nYou decide to ',
        title: "walk_into_cockpit",
      },
    ],
    [
      "Return to your seat",
      {
        desc: "You call on the flight attendant or just settle down in your seat.\nYou decide to ",
        title: "return_seat",
      },
    ],
  ]);
  const scrollRef = useRef();
  const [scroll, setScroll] = useState(0);

  const storyHistory = storyline.map((para) => {
    return <p>{para}</p>;
  });

  const choiceButtons = choices.map((choice) => {
    return <button className="choice-button">{choice[0]}</button>;
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
}
