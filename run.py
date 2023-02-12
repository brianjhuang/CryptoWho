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

def main(targets):
    if 'all' in targets:
        print('Running entire audit pipeline')
        print("Downloading seed data")
        print("Assessing GPT-3 accuracy on seed videos")
    if 'audit' in targets:
        print("Running audit, please ensure you've logged into your account.")
    if 'test' in targets:
        print("Running test pipeline")
        print("Downloading seed data")
        # Logging variables
        totalLogs = len(os.listdir('logs'))
        logFileName = youtube.LOGS_PATH + '/youtube_download_log_{0}.txt'.format(totalLogs)


        # Set up the settings to log information as we run our build pipeline
        logging.basicConfig(filename=logFileName, 
                filemode='a', 
                level=logging.INFO,
                datefmt='%H:%M:%S',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

        seed_data = pd.read_csv('test/youtube/video_ids.csv')
        video_ids = seed_data['video_id']
        labels = seed_data['label']
                
        # Create downloader, list for videos, file_id
        downloader = Downloader()
        videos = []
        file_id = len(os.listdir(youtube.SEED_VIDEOS)) - 1

        print("Starting download...")
        logging.info("Starting download...")
        start = time.time()

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

        df.to_csv(youtube.SEED_VIDEOS + 'test_videos_{0}.csv'.format(file_id), index_label=False)

        print("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'test_videos_{0}.csv'.format(file_id)))
        logging.info("Saved file to:  {0}".format(youtube.SEED_VIDEOS + 'test_videos_{0}.csv'.format(file_id)))

        print("Assessing GPT-3 accuracy on test seed videos")


if __name__ == '__main__':
    targets = [target.lower() for target in sys.argv[1:]]

    main(targets)
    logging.info('END OF BUILD.\n')