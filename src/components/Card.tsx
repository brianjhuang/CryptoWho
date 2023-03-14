import React, { useState } from "react";

type CardProps = {
  topText: string;
  bottomText: string;
};

const Card = ({ topText, bottomText }: CardProps) => {
  const [flipped, setFlipped] = useState(false);

  const handleClick = () => {
    setFlipped(!flipped);
  };

  return (
    <div className={`card ${flipped ? "flipped" : ""}`} onClick={handleClick}>
      <div className="front">
        <img
          src={process.env.PUBLIC_URL + "/images/user_card.png"}
          alt="front image"
          style={{ width: "100%", height: "auto" }}
        />
      </div>

      <div className="back">
        <p style={{ color: "black", fontSize: 12 }}>
          <b>
            <span style={{ fontSize: 17.5, color: "black" }}>{topText}</span>
          </b>
          <br></br>
          {bottomText}
        </p>
      </div>
    </div>
  );
};

export default Card;
