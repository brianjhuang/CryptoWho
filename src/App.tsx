import React from "react";
import { useRef, useEffect } from "react";
import "./App.css";

import Button from "@mui/material/Button";
import GitHubIcon from "@mui/icons-material/GitHub";
import { animated, Interpolation, useSpring } from '@react-spring/web'
import { Parallax, ParallaxLayer, IParallax } from "@react-spring/parallax";

function App() {
  const parallax = useRef<IParallax>(null!)

  return (
    <>
    <Parallax ref = {parallax} pages={3}>
      <ParallaxLayer>Webpage still under development</ParallaxLayer>
    </Parallax>
      <section>
        <h1 style={{ fontSize: 50}}>
          CryptoWho
          <strong
            style={{
              display: "block",
              fontSize: "40%",
              color: "#CCD1D1",
              opacity: 0.75,
            }}
          >
            Who is seeing cryptocurrency content on YouTube?
            <strong
              style={{
                display: "block",
                fontSize: "75%",
                color: "#fffff",
              }}
            >
              by Brian Huang, Lily Yu
            </strong>
          </strong>
          <Button
            variant="contained"
            startIcon={<GitHubIcon />}
            onClick={() =>
              window.open("https://github.com/brianjhuang/CryptoWho", "_blank")
            }
          >
            GitHub
          </Button>
        </h1>
      </section>

      <section>
        <h2>What is this, and why do should I care?</h2>
        <p>{"Lorem Ipsum :)"}</p>
      </section>

      <section>
        <h2>Where is your data from?</h2>
        <p>{"Lorem Ipsum :)"}</p>
      </section>

      <section>
        <h2>How did you do this?</h2>
        <p>{"Lorem Ipsum :)"}</p>
      </section>

      <section>
        <h2>Results</h2>
        <p>{"Lorem Ipsum :)"}</p>
      </section>

      <section>
        <h2>Conclusion</h2>
        <p>{"Lorem Ipsum :)"}</p>
      </section>
    </>
  );
}

export default App;
