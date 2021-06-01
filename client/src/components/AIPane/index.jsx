import React, { useState } from "react";
import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

export default function AIPane() {
  const [visibleHint, setVisibleHint] = useState(false);
  const [hintsLeft, setHintsLeft] = useState(3);

  const toggleHint = async (e) => {
    e.preventDefault();
    if (visibleHint) {
      setVisibleHint(false);
    } else if (hintsLeft > 0) {
      setVisibleHint(true);
      setHintsLeft(hintsLeft - 1);
    }
  };

  return (
    <section className="right-section">
      <div className="right-section-content">
        {visibleHint && (
          <p className="speech-bubble">
            Ahoy! this is the ghost of Napoleon here to guide you!
          </p>
        )}
        <button id="show-hint-button" onClick={toggleHint}>
          <p>Hint</p>
        </button>
        <img src={ghost_of_napoleon} alt="Ghost of Napoleon" id="ai_img" />
      </div>
    </section>
  );
}
