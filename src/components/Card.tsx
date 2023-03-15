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
// margin:"auto", width: (window.innerHeight > window.innerWidth) ? "100%" : "60%"
  return (
    <div className={`card ${flipped ? "flipped" : ""}`} onClick={handleClick} style= {{ width: "100%" }}>
      <div className="front">
        <img
          src={process.env.PUBLIC_URL + "/images/user_card.png"}
          alt="front image"
          style={{ width: "100%", height: "auto" }}
        />
      </div>

      <div className="back">
        { window.outerHeight > window.length ? 
        <p style={{ color: "black", fontSize: 12 }}>
          <b>
            <span style={{ fontSize: 15, color: "black" }}>{topText}</span>
          </b>
          <br></br>
          {bottomText}
        </p>
        :
        <p style={{ color: "black", fontSize: 20 }}>
          <b>
            <span style={{ fontSize: 15, color: "black" }}>{topText}</span>
          </b>
          <br></br>
          {bottomText}
        </p>
        }
      </div>
    </div>
  );
};

export default Card;