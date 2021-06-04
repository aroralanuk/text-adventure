import React, { useState, useEffect } from "react";
import MetricGauge from "../MetricGauge/index";
import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

export default function AIPane({
  hint,
  restarted,
  currSurvival,
  hintTaken,
  trust,
  mood,
}) {
  const [visibleHint, setVisibleHint] = useState(false);
  const [hintsLeft, setHintsLeft] = useState(3);

  useEffect(() => {
    setVisibleHint(false);
    if (restarted) {
      setHintsLeft(3);
    }
  }, [hint, restarted]);

  const giveHint = () => {
    console.log(hint[0]);
    if (hint) {
      return "'" + hint + "' be yer best choice here.";
    } else {
      return "Free will be a figment o' our imagination, init?";
    }
  };

  const toggleHint = async (e) => {
    e.preventDefault();

    if (visibleHint) {
      setVisibleHint(false);
    } else if (hintsLeft > 0) {
      setVisibleHint(true);
      if (hint && hint.length != 0) {
        console.log("hint got: " + hint);
        hintTaken();
        setHintsLeft(hintsLeft - 1);
      }
    }
  };

  return (
    <section className="right-section">
      <div className="ghost-of-napoleon">
        {0 && visibleHint ? (
          <p className="speech-bubble">{giveHint()}</p>
        ) : (
          <p className="speech-bubble">
            Ahoy! this is the ghost of Napoleon here to guide you! You have{" "}
            {hintsLeft} hints left.
          </p>
        )}
        <button id="show-hint-button" onClick={toggleHint}>
          <p>Hint</p>
        </button>
        <img src={ghost_of_napoleon} alt="Ghost of Napoleon" id="ai_img" />
      </div>
      <div className="mood-gauge">
        <MetricGauge
          key="linearGauge"
          gaugeType="LINEAR"
          width={75}
          height={200}
          value={mood}
          title="MOOD"
        />
      </div>
      <div className="radial-gauges">
        <MetricGauge
          key="accuracyGauge"
          gaugeType="RADIAL"
          width={200}
          height={200}
          value={currSurvival}
          title="SURVIVAL"
        />
        <MetricGauge
          key="trustGauge"
          gaugeType="RADIAL"
          width={200}
          height={200}
          value={trust}
          title="TRUSTWORTHINESS"
        />
      </div>
    </section>
  );
}
