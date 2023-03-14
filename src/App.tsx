import React from "react";
import { useRef, useEffect } from "react";
import "./App.css";

import Button from "@mui/material/Button";
import GitHubIcon from "@mui/icons-material/GitHub";

import { animated, Interpolation, useSpring } from "@react-spring/web";
import { Parallax, ParallaxLayer, IParallax } from "@react-spring/parallax";
import { Fade, Slide, Zoom } from "react-awesome-reveal";

import Card from "./components/Card";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const options: ChartOptions<any> = {
  indexAxis: "y" as const,
  elements: {
    bar: {
      borderWidth: 2,
    },
  },
  maintainsAspectRatio: true,
  responsive: true,
  scales: {
    y: {
      ticks: {
        color: "white",
        beginAtZero: true,
        font: {
          size: 20,
        },
      },
    },
    x: {
      ticks: {
        color: "white",
        beginAtZero: true,
        font: {
          size: 20,
        },
      },
    },
  },
  plugins: {
    legend: {
      labels: {
        color: "white",
        font: {
          size: 14,
        },
      },
    },
    title: {
      display: true,
      text: "Top Frauds by reported cryptocurrency losses",
      color: "white", // set the text color to white
      font: {
        size: 16,
      },
    },
  },
};

const labels = [
  "Investment Related Fraud",
  "Romance Scams",
  "Business Imposters",
  "Government Imposters",
];

export const data = {
  labels,
  datasets: [
    {
      label: "Losses in US Dollars",
      data: [575000000, 185000000, 93000000, 40000000],
      borderColor: "rgb(255, 0, 135)",
      backgroundColor: "rgba(255, 0, 0, 0.5)",
    },
  ],
};

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
            <h1 style={{ fontSize: 60, zIndex: 1000 }}>
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
          </section>
        </ParallaxLayer>

        <ParallaxLayer offset={1} speed={0.4}>
          <section>
            <Fade duration={2000} cascade damping={0.15}>
              <h1 style={{ fontSize: 60, color: "red" }}>$1,000,000,000</h1>
              <h1>
                That's how much money has been lost to cryptocurrency scams
                since 2021.
              </h1>
              <h1>
                Over <span style={{ fontSize: 40, color: "red" }}>50%</span> of
                victims reported that their first interaction with
                cryptocurrency was on social media.
              </h1>
              <h1>
                Of those victims, people between{" "}
                <span style={{ color: "red" }}> ages 20-49 </span> were{" "}
                <span style={{ color: "red", fontSize:40 }}> 3x </span> more
                likely to report these types of fraud.
              </h1>
            </Fade>
            <Fade delay={1000}>
              {" "}
              <div
                style={{
                  width: "800px",
                  height: "600px",
                  alignContent: "center",
                  textAlign: "center",
                }}
              >
                <Bar data={data} options={options} />
                January 2021 - March 2022, data sourced from the Federal Trade
                Comission
                <br></br>
                <br></br>
                <h1>
                  With the recent rise of{" "}
                  <span style={{ color: "red" }}>‘Finfluencers’</span> across
                  all platforms, more and more people turn to social media for
                  their personal finances.{" "}
                  <span style={{ color: "red" }}>
                    Can we trust these platforms to provide balanced
                    recommendations to everyone?
                  </span>
                </h1>
              </div>
              <br></br>
              <br></br>
            </Fade>
            <Fade delay={2000}>
              <p>
                Logan Paul's failed 'CryptoZoo' project cost his audience over{" "}
                <span style={{ fontSize: 20, color: "red" }}>$5 million.</span>
              </p>
            </Fade>
            <Fade delay={1000}>
              <img
                style={{
                  width: "1000px",
                  height: "600px",
                }}
                src={process.env.PUBLIC_URL + "/images/sam_and_logan.png"}
              />
              <br></br>
            </Fade>
            <Fade delay={1000}>
              <p style={{ float: "right" }}>
                The collapse of FTX cost lost over
                <span style={{ fontSize: 20, color: "red" }}>$8 billion </span>
                in customer funds.
              </p>
            </Fade>
            <Fade
              delay={1000}
              cascade
              damping={0.1}
              style={{ maxWidth: "600px" }}
            >
              {" "}
              <h1>
                In the following audit, we focus on
                <span style={{ color: "red" }}> You</span>Tube and its rising
                role in education. More and more young people rely on{" "}
                <span style={{ color: "red" }}> You</span>Tube for their
                personal finance. Are these younger watchers being recommended
                the same type of investments as their older peers? Does age have
                any impact on if you see blockchain content?
              </h1>
              <h1>Let's meet our 'users' for our audit.</h1>
            </Fade>
          </section>
        </ParallaxLayer>

        <ParallaxLayer offset={2.5} speed={0.4}>
          <section>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                maxWidth: "1200px",
                margin: "0 auto",
              }}
            >
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(3, 1fr)",
                  gap: "20px",
                  marginBottom: "20px",
                }}
              >
                <Fade delay={1000} cascade damping={0.15} direction="left">
                  {" "}
                  <Card
                    topText={"Young Blockchain Investor"}
                    bottomText={
                      "Our young blockchain expert is around 18-23. Alongside their deep interest in blockchain investments (crypto, NFTs, etc.), they also watch videos about life lesson for teenagers, college decisions and tips, teen dating advice etc."
                    }
                  />
                  <Card
                    topText={"Average Young Investor"}
                    bottomText={
                      "Our young investor is around 18-23. Alongside their deep interest in both blockchain and traditional investments, they also watch videos about life lesson for teenagers, college decisions and tips, teen dating advice etc."
                    }
                  />
                  <Card
                    topText={"Young Traditional Investor"}
                    bottomText={
                      "Our young traditional investor is around 18-23. Alongside their deep interest in traditional investments (stocks, bonds, commodities, etc.) they also watch videos about life lesson for teenagers, college decisions and tips, teen dating advice etc."
                    }
                  />
                </Fade>
              </div>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(3, 1fr)",
                  gap: "20px",
                }}
              >
                <Fade delay={500} cascade damping={0.15} direction="right">
                  {" "}
                  <Card
                    topText={"Old Blockchain Investor"}
                    bottomText={
                      "Our old blockchain investor is around 55-60. Alongside their deep interest in blockchain investments (crypto, NFTs, etc.), they also watch videos about parenting their own teenagers, activities to do when you’re 50+, and age related procedures (colonoscopies)."
                    }
                  />
                  <Card
                    topText={"Average Old Investor"}
                    bottomText={
                      "Our old investor is around 55-60. Alongside their deep interest in both blockchain and traditional investments, they also watch videos about parenting their own teenagers, activities to do when you’re 50+, and age related procedures (colonoscopies)."
                    }
                  />
                  <Card
                    topText={"Old Traditional Investor"}
                    bottomText={
                      "Our old investor is around 55-60. Alongside their deep interest in traditional investments (stocks, bonds, commodities, etc.) they also watch videos about parenting their own teenagers, activities to do when you’re 50+, and age related procedures (colonoscopies)."
                    }
                  />
                </Fade>
              </div>
              <Fade style={{ textAlign: "center" }}>
                <h1>
                  Each of the user's in our audit is split based on one of two
                  criteria:
                </h1>
                <h2>
                  <span style={{ color: "green" }}>Age:</span> We want to know
                  if age impacts your financial recommedations!
                </h2>
                <h2>
                  <span style={{ color: "green" }}>Watch Behavior:</span> What
                  videos is our user looking for? Are they getting recommended
                  similar videos based on what they watch?
                </h2>
                <h2>
                  Regardless of user age, we expect users with similar watch
                  behavior to receive a similar distribution of recommendations!
                </h2>
              </Fade>
            </div>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={3}>
          {" "}
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <br></br>
            <h2>How did you do this?</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={4}>
          {" "}
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <br></br>
            <h2>Results</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
          </section>
        </ParallaxLayer>
        <ParallaxLayer offset={5}>
          <section
            style={{
              backgroundColor: "#000000",
            }}
          >
            <br></br>
            <h2>Conclusion</h2>
            <p>{"Lorem Ipsum :)"}</p>
            <br></br>
            <Button
              variant="contained"
              size="small"
              onClick={() => parallax.current.scrollTo(0)}
            >
              Return to Top
            </Button>
          </section>
        </ParallaxLayer>
      </Parallax>
    </div>
  );
}

export default App;
