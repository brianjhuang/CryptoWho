import sys
# Provide access to main dir path for config, data, etc
sys.path.insert(0, '../../')

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

    video_id = None

    def __init__(self, max_comments = 200):

        self.max_comments = max_comments

        if self.keyExists():
            try:
                self.youtube_api = build(youtube.YOUTUBE_API_SERVICE_NAME, youtube.YOUTUBE_API_VERSION, developerKey=youtube.YOUTUBE_DATA_API_KEY)
                self.transcriber = YouTubeTranscriptApi()
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

    def setVideoId(self, video_id):
        """ Set our video id

        Parameters
        ----------
        video_id : str
            The video_id for the YouTube video, usually found at the end of the URL.
        
        Returns
        -------
        bool
            If we have succesfully set our video ID
        """

        try:
            self.video_id = video_id
            return True
        except:
            return False

    def getVideoId(self):
        """ Get our video id

        Returns
        -------
        str
            Our current video id
        """
        return self.video_id

    def getVideoMetadata(self):
        """Download video meta data given an ID

        Method queries the YouTube Data API and retrieves details of the video. These
        details are used as the video desc, title and tags.

        Parameters
        ----------
        video_id : str
            The video_id for the YouTube video, usually found at the end of the URL.

        Returns
        -------
        dict
            A dictionary with the video desc, title and video tags
        """
        try:
            response = (
                self.youtube_api.videos()
                .list(part="id,snippet,contentDetails", id=self.video_id)
                .execute()
            )
            print(response)
            # Get Video Details
            try:
                videoContent = response["items"][0]

                if "snippet" in videoContent.keys():
                    videoSnippet = videoContent["snippet"]

                    return {
                        "title": videoSnippet["title"],
                        "description": videoSnippet["description"],
                        "tags": videoSnippet["tags"],
                    }

            except:
                return {"title": "", "description": "", "tags": []}

        except (HttpError, SocketError) as error:
            print(
                "--- HTTP Error occurred while retrieving meta data for VideoID: {0}. [ERROR]: {1}".format(
                    self.video_id, error
                )
            )
            return {"title": "", "description": "", "tags": []}

    def getVideoComments(self):
        """Download video comments given an ID

        Method queries the YouTube Data API and retrieves the top comments of a video.

        Parameters
        ----------
        video_id : str
            The video_id for the YouTube video, usually found at the end of the URL.
        num_comments: int
            The max number of comments we want from the video.

        Returns
        -------
        dict
            A dictionary with the comments
        """

        counter = self.max_comments
        nextPageToken = ""
        comments = []

        while counter > 0:
            try:
                # For the first page
                if self.max_comments == counter:
                    response = (
                        self.youtube_api.commentThreads()
                        .list(part="snippet,replies", videoId=self.video_id, maxResults=100)
                        .execute()
                    )
                    print(response)

                    # Grab the ID to the next page
                    if "nextPageToken" in response.keys():
                        nextPageToken = response["nextPageToken"]

                    try:
                        pageComments = []

                        # Get all the comments for the page
                        for item in response["items"]:
                            # Start with the top comment
                            pageComments.append(
                                {
                                    item["snippet"]["topLevelComment"]["id"]: item[
                                        "snippet"
                                    ]["topLevelComment"]["snippet"]["textOriginal"]
                                }
                            )

                            # If we have replies
                            if "replies" in item.keys():
                                # Get all the replies to the comment
                                pageComments += [
                                    {reply["id"]: reply["snippet"]["textOriginal"]}
                                    for reply in item["replies"]["comments"]
                                ]

                        # Each page grabs at max 100 comments
                        counter -= 100
                        comments += pageComments

                    except:
                        return {"comments": []}

                else:
                    # For all subsequent pages
                    response = (
                        self.youtube_api.commentThreads()
                        .list(
                            part="snippet,replies",
                            pageToken=nextPageToken,
                            videoId=self.video_id,
                            maxResults=100,
                        )
                        .execute()
                    )
                    print(response)

                    # Grab the ID to the next page
                    if "nextPageToken" in response.keys():
                        nextPageToken = response["nextPageToken"]

                    try:
                        pageComments = []

                        # Get all the comments for the page
                        for item in response["items"]:
                            # Start with the top comment
                            pageComments.append(
                                {
                                    item["snippet"]["topLevelComment"]["id"]: item[
                                        "snippet"
                                    ]["topLevelComment"]["snippet"]["textOriginal"]
                                }
                            )

                            # If we have replies
                            if "replies" in item.keys():
                                # Get all the replies to the comment
                                pageComments += [
                                    {reply["id"]: reply["snippet"]["textOriginal"]}
                                    for reply in item["replies"]["comments"]
                                ]

                        # Each page grabs at max 100 comments
                        counter -= 100
                        comments += pageComments

                    except:
                        return {"comments": []}

            except (HttpError, SocketError) as error:
                print(
                    "--- HTTP Error occurred while retrieving comments for VideoID: {0}. [ERROR]: {1}".format(
                        self.video_id, error
                    )
                )
                return {"comments": []}

        return {"comments":comments}

    def getVideoTranscript(self):
        """Download video transcript given an ID

        Method uses the youtube-transcript library to query the API for a video_id. Method cleans 
        returned output and provides a text blob back.
        
        Parameters
        ----------
        video_id : str
            The video_id for the YouTube video, usually found at the end of the URL.
        transcriber : YouTubeTranscriptApi
            Our transcription object. Passed in to prevent constant constructor calls.

        Returns
        -------
        dict
            A dictionary with the raw transcript, cleaned transcript, and pauses in the video.
        """

        try:
            raw_transcript = self.transcriber.get_transcript(self.video_id)
        except:
            return {"cleaned_transcript" : "", "raw_transcript" : {}}

        cleaned_transcript = " ".join([phrase['text'] for phrase in raw_transcript])

        return {"cleaned_transcript" : cleaned_transcript, "raw_transcript" : raw_transcript}


if __name__ == '__main__':
    # Get IDs as targets passed through command line
    targets = sys.argv[1:]

    # Create downloader, list for videos, file_id
    downloader = Downloader()
    videos = []
    file_id = len(os.listdir(youtube.RAW_VIDEOS))

    # Collect our data
    for video_id in targets:
        downloader.setVideoId(video_id)
        
        videoMetaData = downloader.getVideoMetadata()
        time.sleep(random.randint(1, 5))
        videoComments = downloader.getVideoComments()
        time.sleep(random.randint(1, 5))
        videoTranscript = downloader.getVideoTranscript()

        video = {
            "title": videoMetaData["title"],
            "description": videoMetaData["description"],
            "tags": videoMetaData["tags"],
            "cleaned_transcript": videoTranscript["cleaned_transcript"],
            "raw_transcript": videoTranscript["raw_transcript"], 
            "comments": [list(comment.values())[0] for comment in videoComments["comments"]],
            "comment_ids" : [list(comment.keys())[0] for comment in videoComments["comments"]],
        }

        videos.append(video)

    df = pd.DataFrame(videos)
    df.to_csv(youtube.RAW_VIDEOS + 'videos_{}.csv'.format(file_id))
