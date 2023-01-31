import sys
# Provide access to main dir path for config, data, etc
sys.path.insert(0, '../../')

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
import sys
import pandas as pd
import re

# Config Imports
from config import reddit


from dataclasses import dataclass
@dataclass
class YoutubeLink:
    url: str
    subreddit: str
    thread_url: str
    
@dataclass
class TextEntry:
    text: str
    subreddit: str
    thread_url: str
    text_type: str