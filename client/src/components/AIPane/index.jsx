import React from "react";
import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

export default function AIPane() {
  return (
    <section className="right-section">
      <div className="right-section-content">
        <p className="speech-bubble">
          Ahoy! this is the ghost of Napoleon here to guide you!
        </p>
        <img src={ghost_of_napoleon} alt="Ghost of Napoleon" id="ai_img" />
      </div>
    </section>
  );
}
