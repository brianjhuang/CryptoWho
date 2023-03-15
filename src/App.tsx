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
    <>
      <div style={{ width: "100%", backgroundColor: "#000000", overflow: "hidden"}}>
        <Parallax ref={parallax} pages={1} style = {{overflow : "hidden"}}>
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
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  flexDirection: "column",
                }}
              >
                <h1 style={{ fontSize: "7vh", zIndex: 1000, margin: "1vh" }}>
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
              </div>
            </section>
          </ParallaxLayer>
        </Parallax>
      </div>
      <div style = {{paddingTop : "100vh"}}>
        <section
          style={{ width: "90vw", margin: "2vh auto", textAlign: "center" }}
        >
          {" "}
          <Fade duration={2000} cascade damping={0.15}>
            <h1 style={{ fontSize: "3vw", color: "red" }}>$1,000,000,000</h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              That's how much money has been lost to cryptocurrency scams since
              2021.
            </h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              Over <span style={{ fontSize: "2.5vh", color: "red" }}>50%</span>{" "}
              of victims reported that their first interaction with
              cryptocurrency was on social media.
            </h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              Of those victims, people between{" "}
              <span style={{ color: "red" }}> ages 20-49 </span> were{" "}
              <span style={{ color: "red", fontSize: "2.7vw" }}> 3x </span> more
              likely to report these types of fraud.
            </h1>
          </Fade>
          <Fade delay={1000}>
            {" "}
            <div
              style={{
                width: "90vw",
                height: "auto",
                alignContent: "center",
                textAlign: "center",
              }}
            >
              <Bar data={data} options={options} />
              January 2021 - March 2022, data sourced from the Federal Trade
              Comission
            </div>
          </Fade>
        </section>

        <section style={{ width: "100vw" }}>
          {" "}
          <Fade style={{ width: "80vw", textAlign: "center" }}>
            {" "}
            <h1 style={{ fontSize: "2.5vh" }}>
              With the recent rise of{" "}
              <span style={{ color: "red" }}>‘Finfluencers’</span> across all
              platforms, more and more people turn to social media for their
              personal finances.{" "}
              <span style={{ color: "red" }}>
                Can we trust these platforms to provide balanced recommendations
                to everyone?
              </span>
            </h1>
          </Fade>
          <Fade delay={2000}>
            <p style={{ textAlign: "center" }}>
              Logan Paul's failed 'CryptoZoo' project cost his audience over{" "}
              <span style={{ color: "red" }}>$5 million.</span>
            </p>
          </Fade>
          <Fade delay={1000}>
            <img
              style={{
                width: "1000px",
                height: "auto",
                maxWidth: "90vw",
              }}
              src={process.env.PUBLIC_URL + "/images/sam_and_logan.png"}
            />
            <br></br>
          </Fade>
          <Fade delay={1000}>
            <p style={{ textAlign: "center" }}>
              The collapse of FTX cost lost over
              <span style={{ color: "red" }}>$8 billion </span>
              in customer funds.
            </p>
          </Fade>
        </section>

        <section>
          <Fade
            cascade
            damping={0.1}
            style={{ width: "95vw", margin: "auto", textAlign: "center" }}
          >
            <h1>
              In the following audit, we focus on
              <span style={{ color: "red" }}> You</span>Tube and its rising role
              in education. More and more young people rely on{" "}
              <span style={{ color: "red" }}> You</span>Tube for their personal
              finance. Are these younger watchers being recommended the same
              type of investments as their older peers? Does age have any impact
              on if you see blockchain content?
            </h1>
            <h1>Let's meet our 'users' for our audit.</h1>
          </Fade>
        </section>

        <section>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, 30vw)",
              gap: "1vw",
              width: "100vw",
              margin: "auto",
              justifyContent: "space-evenly",
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
              <span style={{ color: "green" }}>Age:</span> We want to know if
              age impacts your financial recommedations!
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
        </section>

        <section>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <strong>
              <p style={{ fontSize: "2.5vh" }}>
                {" "}
                <p>
                  We've collected 120 'seed videos' for our users to build their
                  watch histories. Each user will watch 60 of these videos.
                  <br></br>
                </p>
                <p>
                  40 of these videos are used to identify the age of the user to
                  YouTube. (Twenty for each age group)
                  <br></br>
                </p>
                <p>
                  80 of these videos are used to identify what type of videos
                  the user is looking for (40 for the traditional and blockchain
                  labels each.)
                  <br></br>
                </p>
                Our average investor watches the twenty shortest videos from
                each label! Each user watches 50% of the video to demonstrate
                that they have the same interest in all videos!
              </p>
            </strong>
          </Fade>
          <br></br>
          <Fade style={{ maxWidth: "90vw" }}>
            <img
              style={{
                width: "auto",
                height: "auto",
                maxWidth: "90vw",
                borderRadius: "5px",
              }}
              src={process.env.PUBLIC_URL + "/images/audit.png"}
            />
          </Fade>
        </section>

        <section>
          <Fade style={{ textAlign: "center" }}>
            <strong>
              <p style={{ fontSize: "2.5vh" }}>
                As each user watches their videos, we collect the
                recommendations from the side bar and homepage!
                <br></br>
                These recommendations will later be classified using GPT-3.5 to
                determine the distribution of finance videos throughout a user's
                watch period.
              </p>
            </strong>
          </Fade>
          <Fade>
            <img
              style={{
                width: "auto",
                height: "auto",
                maxWidth: "90vw",
                borderRadius: "5px",
              }}
              src={process.env.PUBLIC_URL + "/images/methods.png"}
            />
          </Fade>
        </section>

        <section>
          <Fade style={{ textAlign: "center" }}>
            <strong>
              <p style={{ fontSize: "2.5vh" }}>
                Why GPT?
                <br></br>● Performs much better than any model we can train
                <br></br>● Lack of a large training set (seed videos) meant
                training our own classifier would be difficult
                <br></br>● Interest in prompt‘engineering’ to fine-tune a model
                <br></br>● Through prompting, we can interpret model decisions
                by asking it to explain its rationale
              </p>
            </strong>
          </Fade>
        </section>
      </div>
    </>
  );
}

export default App;
