import sys

import os
import logging
import time
import re

from tqdm import tqdm
import pandas as pd
import random
import datetime

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
    max_comments: int
        The max number of comments we can download.

    Attributes (class)
    -------
    video_id : str
        The current video we're downloading.
    '''

    video_id = None

    def __init__(self, max_comments = 200):

        self.max_comments = max_comments

        if self.keyExists():
            try:
                self.youtube_api = build(youtube.YOUTUBE_API_SERVICE_NAME, youtube.YOUTUBE_API_VERSION, developerKey=youtube.YOUTUBE_DATA_API_KEY)
                self.transcriber = YouTubeTranscriptApi()
                print("Successfully built YouTube API object")
                logging.info("Successfully built YouTube API object")
            except:
                print("Failure to build YouTube API object, are all the values correct/filled in config/YouTube.py?")
                logging.info("Failure to build YouTube API object, are all the values correct/filled in config/YouTube.py?")
        else:
            self.youtube_api = None
            print("Failure to build YouTube API object, are all the values correct/filled in config/YouTube.py?")
            logging.info("Failure to build YouTube API object, are all the values correct/filled in config/YouTube.py?")
    
    def keyExists(self):
        """ Check if we have a key in our environment

        Returns
        -------
        bool
            If we have a key stored in our environment return True 
        """

        return youtube.YOUTUBE_DATA_API_KEY != None

    def apiObjectExists(self):
        """ Check if we have a valid API object

        Returns
        -------
        bool
            If we have a valid API object, return True
        """
        return self.youtube_api != None

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
        details are used as the video desc, title tags, and video duration.

        Parameters
        ----------
        video_id : str
            The video_id for the YouTube video, usually found at the end of the URL.

        Returns
        -------
        dict
            A dictionary with the video desc, title, video tags, and duration
        """
        
        def parse_duration(duration_string):
            # Define regular expression patterns for hours, minutes, and seconds
            hours_pattern = r'(?P<hours>\d+)H'
            minutes_pattern = r'(?P<minutes>\d+)M'
            seconds_pattern = r'(?P<seconds>\d+)S'

            # Extract the components from the duration string using the regular expressions
            hours = 0
            minutes = 0
            seconds = 0

            hours_match = re.search(hours_pattern, duration_string)
            if hours_match:
                hours = int(hours_match.group('hours'))

            minutes_match = re.search(minutes_pattern, duration_string)
            if minutes_match:
                minutes = int(minutes_match.group('minutes'))

            seconds_match = re.search(seconds_pattern, duration_string)
            if seconds_match:
                seconds = int(seconds_match.group('seconds'))

            # Create a time object with the parsed components
            time_obj = datetime.time(hour=hours, minute=minutes, second=seconds)

            return time_obj


            # Create a time object with the parsed components
            time_obj = datetime.time(hour = hours, minute=minutes, second=seconds)

            return time_obj

        if not self.apiObjectExists():
            print("No API object found.")
            logging.info("No API object found.")
            return {"title": "", "description": "", "tags": []}

        try:
            response = (
                self.youtube_api.videos()
                .list(part="id,snippet,contentDetails", id=self.video_id)
                .execute()
            )
            logging.info("Retrieved video meta data response for " + self.video_id)

            # Get Video Details
            try:
                videoContent = response["items"][0]

                if "snippet" in videoContent.keys():
                    videoSnippet = videoContent["snippet"]

                    logging.info("Retrieved video meta data for " + self.video_id)
                    
                    if 'title' in videoSnippet.keys():
                        title = videoSnippet["title"]
                    else:
                        title = ""
                        
                    if 'description' in videoSnippet.keys():
                        description = videoSnippet['description']
                    else:
                        description = ""
                    
                    if 'tags' in videoSnippet.keys():
                        tags = videoSnippet['tags']
                    else:
                        tags = ""
                
                # Get the duration of each video
                if 'contentDetails' in videoContent.keys():
                    videoDetails = videoContent['contentDetails']
                    
                    if 'duration' in videoDetails.keys():
                        raw_duration = videoDetails['duration']
                        duration = parse_duration(raw_duration)
                    else:
                        raw_duration = "PT0H0M0S"
                        duration = datetime.time(hour=0, minute=0, second=0)
                    
                    return {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "raw_duration" : raw_duration,
                        "duration" : duration
                    }

            except:
                logging.info("Meta data was empty or video was missing for " + self.video_id)
                return {"title": "", "description": "", "tags": []}

        except (HttpError, SocketError) as error:
            print(
                "--- HTTP Error occurred while retrieving meta data for VideoID: {0}. [ERROR]: {1}".format(
                    self.video_id, error
                )
            )
            logging.info("--- HTTP Error occurred while retrieving meta data for VideoID: {0}. [ERROR]: {1}".format(
                    self.video_id, error
                ))
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

        if not self.apiObjectExists():
            print("No API object found.")
            logging.info("No API object found.")
            return {"comments": []}

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

                    logging.info("Retrieved video comments response for page one of  " + self.video_id)

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
                        logging.info("Retrieved video comments for page one of  " + self.video_id)
                        comments += pageComments

                    except:
                        logging.info("Comments missing or not available for " + self.video_id)
                        comments += []

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
                    logging.info("Retrieved video comments response for " + self.video_id)

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
                        logging.info("Retrieved video comments for " + self.video_id)
                        comments += pageComments

                    except:
                        logging.info("Comments missing or not available for " + self.video_id)
                        comments += []

            except (HttpError, SocketError) as error:
                print(
                    "--- HTTP Error occurred while retrieving comments for VideoID: {0}. [ERROR]: {1}".format(
                        self.video_id, error
                    )
                )
                logging.info("--- HTTP Error occurred while retrieving comments for VideoID: {0}. [ERROR]: {1}".format(
                        self.video_id, error
                    ))
                return {"comments": []}

        logging.info("Top " + str(self.max_comments) + " comments downloaded for " + self.video_id)
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

        if not self.apiObjectExists():
            print("No API object found.")
            logging.info("No API object found.")
            return {"cleaned_transcript" : "", "raw_transcript" : {}}

        try:
            raw_transcript = self.transcriber.get_transcript(self.video_id)
            logging.info("Retrieved video transcript data for " + self.video_id)
        except:
            logging.info("No video transcript data for " + self.video_id)
            return {"cleaned_transcript" : "", "raw_transcript" : {}}
        
        def clean_transcript(phrase):
            """Clean our transcript"""
            phrase = phrase.strip("\n ")
            logging.info(f"Cleaning following phrase: {phrase}")
            return phrase
        
        def add_pauses(phrase):
            """For transcripts with no natural pauses, add periods."""
            phrase = phrase + ". "
            logging.info(f"Cleaning following phrase: {phrase}")
            return phrase

        cleaned_transcript = " ".join([clean_transcript(phrase['text']) for phrase in raw_transcript]).strip(" \n")
        
        # We can't summarize videos with no sentences and should summarize videos with more than five sentences
        if len(cleaned_transcript.split('. ')) <= youtube.SENTENCE_CUTOFF:
            cleaned_transcript = " ".join([add_pauses(clean_transcript(phrase['text'])) for phrase in raw_transcript]).strip(" \n")

        logging.info("Cleaned and return transcript data for " + self.video_id)
        return {"cleaned_transcript" : cleaned_transcript, "raw_transcript" : raw_transcript}


if __name__ == '__main__':

    # Logging variables
    totalLogs = len(os.listdir('logs'))
    logFileName = youtube.LOGS_PATH + '/youtube_download_log_{0}.txt'.format(totalLogs)


    # Set up the settings to log information as we run our build pipeline
    logging.basicConfig(filename=logFileName, 
            filemode='a', 
            level=logging.INFO,
            datefmt='%H:%M:%S',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
            
    # Get IDs as targets passed through command line
    targets = sys.argv[1:]

    # Create downloader, list for videos, file_id
    downloader = Downloader()
    videos = []
    file_id = len(os.listdir(youtube.EXTERNAL_VIDEOS)) - 1

    print("Starting download...")
    logging.info("Starting download...")
    start = time.time()

    # Collect our data, Added TQDM progress bar
    for i in tqdm(range(len(targets))):

        video_id = targets[i]

        logging.info("Downloading " + video_id)

        downloader.setVideoId(video_id)
        
        videoMetaData = downloader.getVideoMetadata()
        time.sleep(random.randint(1, 5))
        videoComments = downloader.getVideoComments()
        time.sleep(random.randint(1, 5))
        videoTranscript = downloader.getVideoTranscript()

        video = {
            "video_id": video_id,
            "title": videoMetaData["title"],
            "description": videoMetaData["description"],
            "tags": videoMetaData["tags"],
            "cleaned_transcript": videoTranscript["cleaned_transcript"],
            "raw_transcript": videoTranscript["raw_transcript"], 
            "comments": [list(comment.values())[0] for comment in videoComments["comments"]],
            "comment_ids" : [list(comment.keys())[0] for comment in videoComments["comments"]],
        }

        videos.append(video)

        logging.info("Finished downloading " + video_id)

    df = pd.DataFrame(videos)

    print("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))

    df.to_csv(youtube.EXTERNAL_VIDEOS + 'videos_{0}.csv'.format(file_id), index_label=False)

    print("Saved file to:  {0}".format(youtube.EXTERNAL_VIDEOS + 'videos_{0}.csv'.format(file_id)))
    logging.info("Saved file to:  {0}".format(youtube.EXTERNAL_VIDEOS + 'videos_{0}.csv'.format(file_id)))
