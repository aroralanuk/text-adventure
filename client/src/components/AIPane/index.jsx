import React from "react";
import ghost_of_napoleon from "../../images/ghost_of_napoleon.png";
import "./styles.css";

export default function AIPane({ hint }) {
  const giveHint = () => {
    console.log(hint);
    if (hint) {
      return "'" + hint + "' be yer best choice here.";
    } else {
      return "Ahoy! this is the ghost of Napoleon here to guide you!";
    }
  };

  return (
    <section className="right-section">
      <div className="right-section-content">
        {console.log(hint)}
        <p className="speech-bubble">{giveHint()}</p>
        <img src={ghost_of_napoleon} alt="Ghost of Napoleon" id="ai_img" />
      </div>
    </section>
  );
}
