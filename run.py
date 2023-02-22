#!/usr/bin/env python

import sys
import os
import json
import time
import logging
import logging.handlers

from tqdm import tqdm
import pandas as pd
import random

from src.data.youtubeDownloader import Downloader
from src.data.config import youtube

# Logging variables
totalLogs = len(os.listdir('logs'))
logFileName = 'logs/log_{0}.txt'.format(totalLogs)


# Set up the settings to log information as we run our build pipeline
logging.basicConfig(filename=logFileName, 
        filemode='a', 
        level=logging.INFO,
        datefmt='%H:%M:%S',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

def downloadYoutubeData(load_path, test = False):
    '''
    Download on YouTube title, transcript, comments, and tags.
    Returns a dataframe with the video info and label.

    Parameters
    ----------
    load_path : str
        The path to our seed videos.
    test : bool
        If we are running this downloader on test data.
    
    Returns
    -------
    pd.DataFrame
        Our downloaded and labeled data.
    '''

    # Logging variables
    totalLogs = len(os.listdir('logs'))
    logFileName = youtube.LOGS_PATH + '/youtube_download_log_{0}.txt'.format(totalLogs)

    # Set up the settings to log information as we run our build pipeline
    logging.basicConfig(filename=logFileName, 
            filemode='a', 
            level=logging.INFO,
            datefmt='%H:%M:%S',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

    seed_data = pd.read_csv(load_path)
    video_ids = seed_data['video_id']
    labels = seed_data['label']
            
    # Create downloader, list for videos, file_id
    downloader = Downloader()
    videos = []
    file_id = len(os.listdir(youtube.SEED_VIDEOS)) - 1

    print("Starting download...")
    logging.info("Starting download...")
    start = time.time()

    if not downloader.apiObjectExists():
        print("API object not found")
        logging.info("API object not found")
        return pd.DataFrame()

    # Collect our data, Added TQDM progress bar
    for i in tqdm(range(len(video_ids))):

        video_id = video_ids[i]
        label = labels[i]

        logging.info("Downloading " + video_id)

        downloader.setVideoId(video_id)
        
        videoMetaData = downloader.getVideoMetadata()
        time.sleep(random.randint(1, 5))
        videoComments = downloader.getVideoComments()
        time.sleep(random.randint(1, 5))
        videoTranscript = downloader.getVideoTranscript()

        video = {
            "id": video_id,
            "title": videoMetaData["title"],
            "description": videoMetaData["description"],
            "tags": videoMetaData["tags"],
            "cleaned_transcript": videoTranscript["cleaned_transcript"],
            "raw_transcript": videoTranscript["raw_transcript"], 
            "comments": [list(comment.values())[0] for comment in videoComments["comments"]],
            "comment_ids" : [list(comment.keys())[0] for comment in videoComments["comments"]],
            "label": label,
        }

        videos.append(video)

        logging.info("Finished downloading " + video_id)

    df = pd.DataFrame(videos)

    print("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))

    if test:
        df.to_csv(youtube.SEED_VIDEOS + 'test_videos_{0}.csv'.format(file_id), index_label=False)

        print("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'test_seed_videos_{0}.csv'.format(file_id)))
        logging.info("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'test_seed_videos_{0}.csv'.format(file_id)))
    else:
        df.to_csv(youtube.SEED_VIDEOS + 'seed_videos_{0}.csv'.format(file_id), index_label=False)

        print("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'seed_videos_{0}.csv'.format(file_id)))
        logging.info("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'seed_videos_{0}.csv'.format(file_id)))

    return df

def processAgeVideos(load_path, test = False):
    '''
    Create the links for the two age bucket videos and 
    return it as a dataframe.

    Parameters
    ----------
    load_path : str
        The path to our age videos.
    test : bool
        If we are running this for the test target.
    
    Returns
    -------
    pd.DataFrame
        The old and young age videos
    '''

    old = pd.DataFrame()
    young = pd.DataFrame()

    return (old, young)

def audit():
    return

def finetune_davinci():
    return

def finetuned_classifier():
    return

def binary_classifier():
    return

def prompted_classifier():
    return

def main(targets):
    if 'all' in targets:
        print('Running entire pipeline.')
        logging.info('Running entire pipeline.')

        print("Downloading seed data")
        logging.info("Downloading seed data")
        downloadYoutubeData(youtube.RAW_SEED_DATA)

        print("Creating and seperating age bucket videos.")
        logging.info("Creating and seperating age bucket videos.")
        processAgeVideos(youtube.RAW_AGE_DATA)

        print("Running audit, please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit, please ensure you've logged into the account you're auditing with.")
        audit()

        print("Assessing GPT-3 accuracy on test seed videos")
        logging.info("Assessing GPT-3 accuracy on test seed videos")
        ### Add abiltiy to switch between fine tuned, binary, and baseline GPT classifier

    if 'audit' in targets:
        print("Running audit, please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit, please ensure you've logged into the account you're auditing with.")
        audit()
        
    if 'seed' in targets:
        print("Downloading seed data")
        downloadYoutubeData(youtube.RAW_SEED_DATA)

        print("Creating and seperating age bucket videos.")
        logging.info("Creating and seperating age bucket videos.")
        processAgeVideos(youtube.RAW_AGE_DATA)

    if 'test' in targets:
        print("Running test pipeline")
        logging.info("Running test pipeline")
        
        print("Downloading seed data")
        logging.info("Downloading seed data")
        downloadYoutubeData(youtube.TEST_DATA, test = True)

        print("Creating and seperating age bucket videos.")
        logging.info("Creating and seperating age bucket videos.")
        processAgeVideos(youtube.RAW_AGE_DATA, test = True)

        print("Running audit, please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit, please ensure you've logged into the account you're auditing with.")
        # Note we do not run the audit on a test run

        print("Assessing GPT-3 accuracy on test seed videos")
        logging.info("Assessing GPT-3 accuracy on test seed videos")


if __name__ == '__main__':
    targets = [target.lower() for target in sys.argv[1:]]

    main(targets)
    logging.info('END OF BUILD.\n')