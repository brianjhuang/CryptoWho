import React from "react";
import { useRef, useEffect, useState } from "react";
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
      <div
        style={{
          width: "100%",
          backgroundColor: "#000000",
          overflow: "hidden",
        }}
      >
        <Parallax ref={parallax} pages={1} style={{ overflow: "hidden" }}>
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
      <div style={{ paddingTop: "100vh" }}>
        <section
          style={{ width: "90vw", margin: "2vh auto", textAlign: "center" }}
        >
          {" "}
          <Fade duration={2000} cascade damping={0.15}>
            <h1 style={{ fontSize: "5vh", color: "red" }}>$1,000,000,000</h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              That's how much money has been lost to cryptocurrency scams since
              2021.
            </h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              Over <span style={{ fontSize: "3vh", color: "red" }}>50%</span> of
              victims reported that their first interaction with cryptocurrency
              was on social media.
            </h1>
            <h1 style={{ fontSize: "2.5vh" }}>
              Of those victims, people between{" "}
              <span style={{ fontSize: "3vh", color: "red" }}>
                {" "}
                ages 20-49{" "}
              </span>{" "}
              were <span style={{ color: "red", fontSize: "3h" }}>
                {" "}
                3x{" "}
              </span>{" "}
              more likely to report these types of fraud.
            </h1>
          </Fade>
          <Fade delay={1000}>
            {" "}
            <div
              style={{
                width: "50vw",
                height: "auto",
                alignContent: "center",
                textAlign: "center",
              }}
            >
              <Bar data={data} options={options} />
              January 2021 - March 2022, data sourced from the Federal Trade
              Comissions
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
          <Fade delay={1500}>
            <p style={{ textAlign: "center" }}>
              Logan Paul's failed 'CryptoZoo' project cost his audience over{" "}
              <span style={{ color: "red" }}>$5 million.</span>
            </p>
          </Fade>
          <Fade delay={1000}>
            <img
              style={{
                width: "800px",
                height: "auto",
                maxWidth: "90vw",
              }}
              src={process.env.PUBLIC_URL + "/images/sam_and_logan.png"}
            />
            <br></br>
          </Fade>
          <Fade delay={500}>
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
              In the following project, we focus on
              <span style={{ color: "red" }}> You</span>Tube and its rising role
              in financial education.
            </h1>
            <p>
              More and more young people rely on{" "}
              <span style={{ color: "red" }}> You</span>Tube for their personal
              finance. Are these younger watchers being recommended the same
              type of investments as their older peers? Does age have any impact
              on if you see blockchain content?
              <br></br>
              <span style={{ color: "red" }}> You</span>Tube is innocent until
              proven guilty, so we assume that all recommendations are based on
              watch behavior alone, and regardless of age, users will receive a
              similar distribution of recommendations.
            </p>
            <h1>Let's meet our viewers...</h1>
          </Fade>
        </section>

        <section>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, 20vw)",
              width: "100vw",
              gap: "1vh",
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
        </section>

        <section>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <p style={{ fontSize: "2.5vh" }}>
              {" "}
              We've collected 120 seed videos for our users to build their watch
              histories. Each user will watch 60 of these videos.
              <br></br>
              40 of these videos are used to identify the age of the user to
              YouTube.
              <br></br>
              20 of these videos are videos we expect people between the ages of
              18-23 to watch, while the other twenty are for people between the
              ages of 55-60.
              <br></br>
              80 of these videos are used to identify a user as either a
              blockchain investor or traditional investor. Each label has 40
              videos.
              <br></br>
              Our average or mixed investor watches the twenty shortest videos
              from each label.
              <br></br>
              Each user watches 50% of the video. This is because YouTube
              factors in watch time, so watching videos unevenly may bias user
              recommendations. If we only watch a small percent of each video,
              YouTube may also think we don't enjoy these types of videos.
            </p>
            <br></br>
          </Fade>

          <section>
            <h2>Here are some examples of our seed videos</h2>
            <div className="grid-container">
              <Fade delay={500} cascade damping={0.25} direction="right">
                <div>
                  <h3>Young</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/wm6Ld8XcdGc"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
                <div>
                  <h3>Old</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/xd1N0WOcd5A"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
                <div>
                  <h3>Traditional</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/lFyeLeP44kY"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
                <div>
                  <h3>Blockchain</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/SSo_EIwHSd4"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
                <div>
                  <h3>Mixed</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/LmHmPeRTNdI"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
                <div>
                  <h3>Unrelated</h3>
                  <iframe
                    width="300"
                    height="150"
                    src="https://www.youtube.com/embed/dQw4w9WgXcQ"
                    title="YouTube video player"
                    allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  ></iframe>
                </div>
              </Fade>
            </div>
          </section>
          <br></br>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <h2>Our audit follows the steps outlined in the image below.</h2>
            <img
              style={{
                width: "800px",
                height: "auto",
                maxWidth: "90vw",
                borderRadius: "5px",
              }}
              src={process.env.PUBLIC_URL + "/images/audit.png"}
            />
            <p>
              Each user watches their set of seed videos to build a watch
              history. The rationale for creating a watch history for each age
              is rooted in the idea that YouTube does not consider the age
              parameter in your account settings. Oftentimes, ages on YouTube
              can be faked, and we assume that YouTube’s recommender system will
              use the videos watched to generate an age bucket rather than
              relying on a user’s inputted age. Following this logic, we do not
              create any accounts. We watch specific finance videos to show
              YouTube our user's interest in a specific topic. Assuming age is
              not a factor, users should expect to see exactly what they're
              looking for.
            </p>
            <p>
              As each user watches their videos, we collect the recommendations
              from the side bar and homepage. These videos are later classifed
              using GPT to determine the distribution of finance videos across a
              user's recommendations.
            </p>
          </Fade>
        </section>

        <section>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <img
              style={{
                width: "800px",
                height: "auto",
                maxWidth: "90vw",
                borderRadius: "5px",
              }}
              src={process.env.PUBLIC_URL + "/images/methods.png"}
            />
          </Fade>
        </section>

        <section>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <strong>
              <h1>Why GPT?</h1>
            </strong>
            <strong>
              <p>
                {" "}
                - Performs much better than any model that can be trained in
                less than 10 weeks.
                <br></br>- Lack of a large training set (seed videos) meant
                training our own classifier would be difficult.
                <br></br>- Interest in prompt "engineering" to fine-tune a model
                for this project.
                <br></br>- Through clever prompting, we can interpret model
                decisions by asking it to explain its rationale.
              </p>
            </strong>
          </Fade>
          <br></br>
        </section>

        <section>
          <br></br>
          <Fade style={{ textAlign: "center", width: "80%" }}>
            <strong>
              <Fade
                cascade
                damping={0.025}
                style={{ fontSize: 20, textAlign: "center", width: "80%" }}
              >
                Using GPT, we reached an astounding classification accuracy of
              </Fade>
              <Fade delay={1750} style={{ textAlign: "center" }}>
                <span style={{ color: "green", fontSize: 40 }}>91%</span>
              </Fade>
            </strong>
          </Fade>
        </section>

        <section>
          <br></br>
          <Fade delay={2000} style={{ textAlign: "center", width: "80%" }}>
            <img
              style={{
                width: "800px",
                height: "auto",
                maxWidth: "90vw",
              }}
              src={process.env.PUBLIC_URL + "/images/confusion_matrix.png"}
            />
          </Fade>
          <br></br>
          <Fade delay={2000} style={{ textAlign: "center", width: "80%" }}>
            This was achieved on our seed video set. Given more time and a
            larger dataset, we believe even higher precision can be achieved
            within our model.
          </Fade>
        </section>

        <section>
          <Fade delay={2000} style={{ textAlign: "center", width: "80%" }}>
            <p>
              Designing prompts was critical to reaching high accuracies in our
              classifier. Unlike traditional classifiers, our seed video set
              functioned both as the set used to create watch history and the
              test set for our classifier. This is due to the fact that GPT-3.5
              does not require a labeled training set (however it does help to
              have more data) to fine-tune/train. In the future, given more
              time, we would like to fine-tune the model using a training set
              and testing set. This is something future researchers can delve
              into when using GPT to audit. Given the relatively short lifetime
              of GPT 3.5, there are many different ways to approach using it as
              a classifier that we did not cover. Starting from GPT 3.5 prompts
              are strung together to create a message. The message is sent to
              the Chat Completions API where we collect our final prediction. In
              all of our prompts, we pass in a YouTube video snippet, which is
              the title concatenated with a summarized transcript (using
              TextRank) and the top video tags determined using TF-IDF. It
              outputs a predicted label with the probabilities and a short
              explanation. We had multiple iterations of different prompts. We
              follow a message format starting with a system message to bias our
              model towards our task, a user message providing details on our
              labels and how-to return formats, and an assistant message to
              reiterate instructions so our classifier is more consistent with
              output. We follow up with one last user message when we make our
              API call containing our video snippet. The API returns a
              completion object with the label and rationale behind its
              prediction.
            </p>
          </Fade>
        </section>

        <section>
          <br></br>
          <br></br>
          <br></br>
        </section>
      </div>
    </>
  );
}

export default App;
