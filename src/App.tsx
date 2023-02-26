import React from "react";

import "./App.css";

function App() {
  return (
    <>
      <section>
        <h1 style={{ fontSize: 50 }}>
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
