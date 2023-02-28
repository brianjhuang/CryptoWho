import React from "react";
import { useRef, useEffect } from "react";
import "./App.css";

import Button from "@mui/material/Button";
import GitHubIcon from "@mui/icons-material/GitHub";
import ExpandCircleDownTwoToneIcon from "@mui/icons-material/ExpandCircleDownTwoTone";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

import { animated, Interpolation, useSpring } from "@react-spring/web";
import { Parallax, ParallaxLayer, IParallax } from "@react-spring/parallax";
import IconButton from "@mui/material/IconButton";

function App() {
  const parallax = useRef<IParallax>(null!);

  return (
    <div style={{ width: "100%", height: "100%", backgroundColor: "#000000" }}>
      <Parallax ref={parallax} pages={6}>
        <ParallaxLayer
          offset={0}
          speed={0}
          style={{
            backgroundImage: `url(${process.env.PUBLIC_URL}/images/cryptowhopainting.png)`,
            backgroundColor: "#000000",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
          }}
        ></ParallaxLayer>

        <ParallaxLayer
          offset={0}
          speed={-0.1}
          style={{
            backgroundImage: `url(${process.env.PUBLIC_URL}/images/cryptowho.png)`,
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
          }}
        ></ParallaxLayer>

        <ParallaxLayer
          offset={0.1}
          speed={0}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <section>
            <h1 style={{ fontSize: 50, zIndex: 1000 }}>
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
                  window.open(
                    "https://github.com/brianjhuang/CryptoWho",
                    "_blank"
                  )
                }
              >
                GitHub
              </Button>
            </h1>
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(1)}
            >
              <ExpandCircleDownTwoToneIcon />
            </IconButton>
          </section>
        </ParallaxLayer>

        <ParallaxLayer offset={1}>
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(0)}
            >
              <ExpandLessIcon />
            </IconButton>
            <br></br>
            <h2>What is this, and why do should I care?</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(2)}
            >
              <ExpandMoreIcon />
            </IconButton>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={2}>
          {" "}
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(1)}
            >
              <ExpandLessIcon />
            </IconButton>
            <br></br>
            <h2>Where is your data from?</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(3)}
            >
              <ExpandMoreIcon />
            </IconButton>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={3}>
          {" "}
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(2)}
            >
              <ExpandLessIcon />
            </IconButton>
            <br></br>
            <h2>How did you do this?</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(4)}
            >
              <ExpandMoreIcon />
            </IconButton>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={4}>
          {" "}
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(3)}
            >
              <ExpandLessIcon />
            </IconButton>
            <br></br>
            <h2>Results</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(5)}
            >
              <ExpandMoreIcon />
            </IconButton>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={5}>
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <IconButton
              color="primary"
              aria-label="Expand More"
              size="large"
              onClick={() => parallax.current.scrollTo(4)}
            >
              <ExpandLessIcon />
            </IconButton>
            <br></br>
            <h2>Conclusion</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <Button
              variant="contained"
              size="small"
              onClick={() => parallax.current.scrollTo(0)}
            >Return to Top</Button>
          </section>
        </ParallaxLayer>
      </Parallax>
    </div>
  );
}

export default App;
