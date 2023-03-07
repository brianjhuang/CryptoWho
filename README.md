# CryptoWho
Data Science Capstone Project advised under Stuart Geiger

## Authors
#### Brian Huang and Lily Yu

## Overview
In 2020, Bitcoin, other Cryptocurrencies and blockchain investments (NFTs) experienced a major boom. With the endorsements of many major companies and what seemed to be a large scale adoption on the horizon, the Crypto craze had started kicking off.

For many, cryptocurrency and NFTs were the first time they encountered an 'investment'. Many proclaimed crypto/NFT traders had no prior experience with any investing (stock market, retirement accounts, etc.) and looked to crypto/NFT as a get rich quick path. However, with the influx of new and young traders it was only a matter of time before the crypto/NFT scams began to pray on it's new consumers.

While crypto/NFT is not inherently a scam, many bad actors began to manipulate the influx of young and inexperienced investors. Many schemes akin to pump and dumps began to appear and with the popularity of crypto/NFT throughout social media, many inexperienced investors were quick to turn a blind eye to scams that seasoned investors may recognize immediately.

Cases like this have occured with traditional markets as well, where investors pour money into an asset based off of hype with no sound reasoning ($GME or GameStop). Crypto/NFTts however were especially susceptible to this with the combination of a relatively new asset, large demographic of young investors, and many social media influencers promoting these assets (Logan Paul, Doja Cat, etc)

With the most recent scandals in the cryptocurrency/NFT world (FTX, Logan Paul's CryptoZoo), it's more important than ever to investigate the platforms that many of these assets are promoted on. While platforms like YouTube and TikTok may not be intentionally promoting this content, it's important that they're aware of if their algorithms do indeed promote this type of content. To clarify, we do not provide an opinion on whether these scams are run by the founders of these products (FTX's Sam Bankman-Fried and CryptoZoo's Logal Paul) but rather emphasize that the scams have occured.

The goal of this project is to investigate YouTube's recommendation algorithm to provide insight on the types of investment recommendations being provided to users across a variety of age groups. We assume that all individuals should be receiving the same proportion of recommendations based on their search trends (within a margin of error) regardless of age. This implies that a user who is younger and searching for general investment advice should not be receiving more crypto/NFT recommendations than someone who is older with similar watch history. By conducting audits on YouTube, we hope to gain valuable insight on YouTube and it's role in propogating this type of content on their platform (whether intentional or not).

### What does this repository offer?

The repository offers all tools used to conduct the audit. Helper functions and classes help download video and metadata from YouTube, run headless browsers to watch seed videos, and query the GPT-3 API for video sentiment classification.

All code can be found in the `src` folder and imported respectively. For any changes in filepath or settings, please look through the `config` folder.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Downloading YouTube Data](#downloading-youtube-video-data)
- [GPT Prompting and Fine-Tuning](#gpt-prompting-and-fine-tuning)
- [Conducting the Audit](#conducting-the-audit)
- [Inference](#running-inference)
- [Generating Audit Results](#generating-audit-results)
## Installation

We are using Python version [3.8.5](https://www.python.org/downloads/release/python-385/).

Please install this version of Python, as gensim summarization is still supported.

Versions between 3.8 and 3.9 should work, however we recommend you install the same version we use.

We recommend using [Anaconda](https://www.anaconda.com/) environments to do so.

**Once you've installed Anaconda, please run the following to create your environment.**

```bash
conda create --name <env_name> python=3.8.5
```

**Activate your conda environment like so:**
```bash
# Linux/Mac
source activate <env_name>

# Windows
activate <env_name>
```

**Install required packages**

```bash
pip install -r requirements.txt
```

**If you have Python 3.8.5 working outside of Conda (or any other version of Python that works with gensim) you can create a normal environment if you prefer**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

**Install required packages**

```bash
pip install -r requirements.txt
```

### Reddit Thread Scraper

We use Selenium with the Firefox Webdriver to conduct our audit and gather YouTube video recommendations.

Note: More recent versions of FireFox will just launch if you have the browser installed. Please install the Firefox browser. If it does not work, install the driver.

To run the scraper, you will need to install the Firefox Webdriver, which can be downloaded [here](https://github.com/mozilla/geckodriver/releases).

To install, place your OS-appropriate executable in a directory locatable by your PATH.

### API Key Setup

Our codebase uses the YouTube Data API to download video metadata, comments, and for many other purposes like searching YouTube and grabbing recommendations. We use the OpenAI API to provide snippets and retrieve classification labels for our downloaded videos.

You can enable the YouTube Data API for your Google account and obtain an API key following the steps <a href="https://developers.google.com/youtube/v3/getting-started">here</a>.

The key can be found after you set up your cloud console.

You can fetch your OpenAI API key from <a href="https://platform.openai.com/here</a>.

The key can be found in your profile under ***View API Keys***.

Once you have both API keys, please set the ```YOUTUBE_DATA_API_KEY``` and ```OPENAI_API_KEY``` variable in your environment:

You can do so by going to your home directory and running the following command:

**Mac OS and Linux**

```
nano .bash_profile

# Note Mac Users using zsh shell users should also set their keys in their zsh_profile
nano .zsh_profile
```

Inside your bash profile, you can go ahead and set this at the top:

```
# YOUTUBE API KEY
export YOUTUBE_DATA_API_KEY="YOUR_API_KEY"
export OPENAI_API_KEY="YOUR_API_KEY"
```

Close out of your terminal and your code editor to see changes occur.

**Check that updates have been made**
```
echo $YOUTUBE_DATA_API_KEY
echo $OPENAI_API_KEY
```

The following tutorials cover how to do this as well:

https://www.youtube.com/watch?v=5iWhQWVXosU&t=1s (Mac/Linux)

https://www.youtube.com/watch?v=IolxqkL7cD8 (Windows)

If you are not seeing updates, your `bash_profile` may not be sourced. To resolve this, add the following line to your `.bashrc`:

```
. ~/.bash_profile

# Note Mac Users using zsh shell users should do this in .zshrc
. ~/.zsh_profile
```

This can be anywhere, but we've put ours at the very bottom. Use the following command to enter your `.bashrc`.

```
nano .bashrc
# Note Mac Users using zsh shell users should do this
nano .zshrc
```

Now within Python you can access your API key by doing the following:
```
import os

youtube_key = os.environ.get("YOUTUBE_DATA_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")
```

## Downloading YouTube Video Data
Using `run.py seed` will download all seed videos and save it in `data/seed/youtube/videos_{}.csv`.

Using `run.py audit` will download all videos from the audit and save the downloaded videos in `data/audit/youtube/videos_{}.csv`.

Calling `python3 src/data/youTubeDownloader.py <video_ids seperated by spaces>` will download any videos you want and save it in `data/external/youtube/videos_{}.csv`. 

## GPT Prompting and Fine Tuning
***TO BE ADDED***

## Conducting the Audit
***TO BE ADDED***

## Running Inference
***TO BE ADDED***

## Generating Audit Results
***TO BE ADDED***
