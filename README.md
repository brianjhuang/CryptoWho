# CryptoWho

## Overview

## Installation

**Create and activate Python >= 3.6 Virtual Environment**

We are using Python version 3.8.5

```bash
python3 -m venv .venv

source .venv/bin/activate
```
**Install required packages**
```bash
pip install -r requirements.txt
```

### YouTube Data API
Our codebase uses the YouTube Data API to download video metadata and for many other purposes like searching YouTube. 
Hence, it is important that you create an API key for the YouTube Data API and set it in the configuration files of our codebase.
You can enable the YouTube Data API for your Google account and obtain an API key following the steps <a href="https://developers.google.com/youtube/v3/getting-started">here</a>.

Once you have a **YouTube Data API Key**, please set the ```YOUTUBE_DATA_API_KEY``` variable in your environment:

You can do so by going to your home directory and running the following command:

**Mac OS**

```
nano .bash_profile
```

Inside your bash profile, you can go ahead and set this at the top:

```
# YOUTUBE API KEY
export YOUTUBE_DATA_API_KEY="YOUR_API_KEY"
```

** Linux **
```
export YOUTUBE_DATA_API_KEY
echo $YOUTUBE_DATA_API_KEY
```

You can un-set your API KEY like so:
```
unset YOUTUBE_DATA_API_KEY
```

The following tutorials cover how to do this as well:

https://www.youtube.com/watch?v=5iWhQWVXosU&t=1s (Mac/Linux)

https://www.youtube.com/watch?v=IolxqkL7cD8 (Windows)

Now within Python you can access your API key by doing the following:
```
import os

os.environ.get("YOUTUBE_DATA_API_KEY")
```
