import React, { useState, useEffect } from "react";
import MetricGauge from "../MetricGauge/index";
import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

export default function AIPane({ hint, restarted }) {
  const [visibleHint, setVisibleHint] = useState(false);
  const [hintsLeft, setHintsLeft] = useState(3);

  useEffect(() => {
    setVisibleHint(false);
    if (restarted) {
      setHintsLeft(3);
    }
  }, [hint, restarted]);

  const giveHint = () => {
    console.log(hint);
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
      if (hint) {
        setHintsLeft(hintsLeft - 1);
      }
    }
  };

  return (
    <section className="right-section">
      <div className="ghost-of-napoleon">
        {visibleHint ? (
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
          value={10}
          title="MOOD"
        />
      </div>
      <div className="radial-gauges">
        <MetricGauge
          key="radialGauge1"
          gaugeType="RADIAL"
          width={200}
          height={200}
          value={10}
          title="SURVIVAL"
        />
        <MetricGauge
          key="radialGauge2"
          gaugeType="RADIAL"
          width={200}
          height={200}
          value={60}
          title="TRUSTWORTHINESS"
        />
      </div>
    </section>
  );
}
