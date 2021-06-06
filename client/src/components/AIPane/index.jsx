import React, { useState, useEffect, useRef } from "react";
import { Icon } from "semantic-ui-react";

import { withStyles, makeStyles } from "@material-ui/core/styles";
import { Tooltip } from "@material-ui/core";

import MetricGauge from "../MetricGauge/index";

import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

const survivalTip =
  "This gauge gives your survival chance at this stage as predicted by the ghost.";
const trustTip =
  "This gauge presents you the ratio of people who agreed with the hint given by the ghost at this stage.";
const moodTip =
  "This slider displays the current mood of the ghost determined by your adherence to his hints. As his mood worsens, he's more likely to give you deceiving hints.";
const hintBtnTip =
  "Click the 'Hints' button to receive a hint from the ghost of Napoleon if you're stuck.";
const ghostTip =
  "The ghost of Napoleon is an AI-powered guide who is ready to give you helpful or not-so-helpful clues at every choice.";

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
  // const [show, setShow] = useState(false);
  const target = useRef(null);

  useEffect(() => {
    setVisibleHint(false);
    if (restarted) {
      setHintsLeft(3);
    }
  }, [hint, restarted]);

  const giveHint = () => {
    if (hint.length) {
      return hint;
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
        console.log(hint);
        hintTaken();
        setHintsLeft(hintsLeft - 1);
      }
    }
  };

  const HtmlTooltip = withStyles((theme) => ({
    tooltip: {
      backgroundColor: "#505050",
      color: "white",
      maxWidth: 220,
      fontSize: "1rem",
      border: "1px solid #dadde9",
    },
  }))(Tooltip);

  const tooltips = (text, direction) => (
    <HtmlTooltip
      title={
        <React.Fragment>
          <div className="tooltips">{text}</div>
        </React.Fragment>
      }
      placement="right"
    >
      <Icon style={{ margin: "0.5rem" }} name="question circle outline" />
    </HtmlTooltip>
  );

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

        {tooltips(hintBtnTip, "right")}

        <img src={ghost_of_napoleon} alt="Ghost of Napoleon" id="ai_img" />
        {tooltips(ghostTip, "left")}
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
        {tooltips(moodTip, "left")}
      </div>

      <div className="radial-gauges">
        {tooltips(survivalTip, "right")}
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
        {tooltips(trustTip, "left")}
      </div>
    </section>
  );
}
