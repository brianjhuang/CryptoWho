import sys

import os
import logging
import json
import time

from tqdm.notebook import tqdm
import pandas as pd
import random

# YouTube API Libraries
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from socket import error as SocketError

# Config Imports
from config import youtube

class Downloader():
    ''' Gets tabular data for YouTube video(s) given id(s)

    Returns tabular data by querying the YouTube API given id(s) for different 
    YouTube video(s). The returned data contains video title, description, tags, 
    top 200 comments (by default) with replies, and transcript (both raw with time stamps between pauses 
    and cleaned transcript).

    Parameters
    ----------
    save_path : str
        The path we want to save the data to.
    set_name : str
        The name of the set we're scraping

    Attributes (class)
    -------
    card_url : str
        The URL of the card we want to scrape.
    card_name : str
        The name of the card

    Attributes (class)
    -------
    card_url : str
        The URL of the card we are currently scraping
    card_name : str
        The name of the card

    '''

    def __init__(self, video_ids = [], video_id = "", scrape_multiple = True, max_comments = 200):
        
        self.scrape_multiple = scrape_multiple

        # Determine if we're just scraping one ID or multiple
        if scrape_multiple:
            self.video_ids = video_ids
        else:
            self.video_id = video_id

        self.max_comments = max_comments

        if self.keyExists():
            try:
                self.youtube_api = build(youtube.YOUTUBE_API_SERVICE_NAME, youtube.YOUTUBE_API_VERSION, developerKey=youtube.YOUTUBE_DATA_API_KEY)
                print("Successfully built YouTube API object")
            except:
                print("Failure to build YouTube API object, are all the values correct/filled in config/YouTube.py?")
    
    def keyExists(self):
        """ Check if we have a key in our environment

        Returns
        -------
        bool
            If we have a key stored in our environment return True 
        """

        return youtube.YOUTUBE_DATA_API_KEY != None