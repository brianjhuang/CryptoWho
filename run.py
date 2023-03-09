#!/usr/bin/env python

import sys
import os
import json
import time
import logging
import logging.handlers
import datetime

from tqdm import tqdm
import pandas as pd
import random
import re
import math

from src.data.youtubeDownloader import Downloader
from src.features.youtubeCleaner import Cleaner
from src.audit.youtubeAudit import run_audit
from src.model.gpt import ChatCompletionModel
from config import youtube, audit, classifier

# Logging variables
totalLogs = len(os.listdir('logs'))
logFileName = 'logs/log_{0}.txt'.format(totalLogs)


# Set up the settings to log information as we run our build pipeline
logging.basicConfig(filename=logFileName, 
        filemode='a', 
        level=logging.INFO,
        datefmt='%H:%M:%S',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

def extract_video_id(url):
    try: 
        # Search for the video id
        match = re.search(r'[?&]v=([^&]*)?', url)

        # If we don't find the video id, try and use a normal split
        if match:
            videoId = match.group(1).split('&')[0]
        else:
            if 'v=' in url:
                videoId = url.split('v=')
                if len(videoId) > 1:
                    videoId = url.split('v=')[1]
                else:
                    videoId = None
            elif 'shorts/' in url:
                videoId = url.split('shorts/')
                if len(videoId) > 1:
                    videoId = url.split('shorts/')[1]
                else:
                    videoId = None
            else:
                videoId = None
    except:
        return None
    return videoId

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
            
    # Create downloader, list for videos
    downloader = Downloader()
    videos = []

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
            "video_id": video_id,
            "title": videoMetaData["title"],
            "description": videoMetaData["description"],
            "tags": videoMetaData["tags"],
            "raw_duration": videoMetaData["raw_duration"],
            "duration": videoMetaData["duration"],
            "cleaned_transcript": videoTranscript["cleaned_transcript"],
            "raw_transcript": videoTranscript["raw_transcript"], 
            "comments": [list(comment.values())[0] for comment in videoComments["comments"]],
            "comment_ids" : [list(comment.keys())[0] for comment in videoComments["comments"]],
            "label": label,
            "link": "www.youtube.com/watch?v=" + video_id,
        }

        videos.append(video)

        logging.info("Finished downloading " + video_id)

    df = pd.DataFrame(videos)

    print("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))

    if test:
        df.to_csv(youtube.INTERIM_VIDEOS + 'test_seed_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_seed_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_seed_videos.csv'))
    else:
        df.to_csv(youtube.INTERIM_VIDEOS + 'seed_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'seed_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'seed_videos.csv'))

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
            "video_id": video_id,
            "title": videoMetaData["title"],
            "description": videoMetaData["description"],
            "tags": videoMetaData["tags"],
            "raw_duration": videoMetaData["raw_duration"],
            "duration": videoMetaData["duration"],
            "cleaned_transcript": videoTranscript["cleaned_transcript"],
            "raw_transcript": videoTranscript["raw_transcript"], 
            "comments": [list(comment.values())[0] for comment in videoComments["comments"]],
            "comment_ids" : [list(comment.keys())[0] for comment in videoComments["comments"]],
            "label": label,
            "link": "www.youtube.com/watch?v=" + video_id,
        }

        videos.append(video)

        logging.info("Finished downloading " + video_id)

    df = pd.DataFrame(videos)

    print("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))

    if test:
        df.to_csv(youtube.INTERIM_VIDEOS + 'test_age_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_age_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_age_videos.csv'))
    else:
        df[df['label'] == 'young'].to_csv(youtube.INTERIM_VIDEOS + 'young_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'young_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'young_videos.csv'))

        df[df['label'] == 'old'].to_csv(youtube.INTERIM_VIDEOS + 'old_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'old_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'old_videos.csv'))

    return df

def createSnippets(load_path, save_path, max_word_count = 250, use_ratio = False, ratio = 0.2):
    '''
    Clean our seed videos. Given a dataframe, save our data to 
    the final seed path folder.

    Parameters
    ----------
    load_path : str
        The path to our seed videos.
    save_path : str
        Where we want to save the output.
    test : bool
        If we are running this downloader on test data.
    
    Returns
    -------
    pd.DataFrame
        Our cleaned data with snippets
    '''

    print(f"""\n Cleaning data with the following settings:
    \n Using Ratio?: {use_ratio}
    \n Ratio: {ratio}
    \n Max Word Count: {max_word_count}
    \n Load Path: {load_path}
    \n Save Path: {save_path}
    """)

    logging.info(f"""\n Cleaning data with the following settings:
    \n Using Ratio?: {use_ratio}
    \n Ratio: {ratio}
    \n Max Word Count: {max_word_count}
    \n Load Path: {load_path}
    \n Save Path: {save_path}
    """)

    df = pd.read_csv(load_path)
    print(f"Read in : {load_path}")
    logging.info(f"Read in : {load_path}")

    cleaner = Cleaner(df, save_path=save_path, max_word_count=max_word_count, use_ratio=use_ratio, ratio=ratio)
    print(f"Cleaning : {load_path}")
    logging.info(f"Cleaning : {load_path}")

    df_with_snippets = cleaner.generateVideoSnippets()

    df_with_snippets.to_csv(save_path, index_label=False)
    print(f"Finished cleaning, saving to : {save_path}")
    logging.info(f"Finished cleaning, saving to : {save_path}")

    return df_with_snippets

def conduct_audit(audits = []):
    if len(audits) <= 0:
        run_audit()
    else:
        for run in audits:
            run_audit(run['type'], run['age'])
            time.sleep(600)

def download_audit_videos(video_ids, save_path, kind):
        
    # store our downloaded videos
    videos = []
    df = pd.DataFrame()
    
    # check for progress
    saved_files = os.listdir(audit.AUDIT_DOWNLOADED_RESULTS_PATH)
    downloader = Downloader()
    
    print("Starting download...")
    logging.info("Starting download...")
    start = time.time()

    if not downloader.apiObjectExists():
        print("API object not found")
        logging.info("API object not found")
        return pd.DataFrame()
    
    if f'{kind}_audit_progress.csv' in saved_files:
        
        print('Progress found, starting from where we left off.')
        logging.info('Progress found, starting from where we left off.')
        progress = pd.read_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + f'{kind}_audit_progress.csv')
        
        progress_video_ids = list(progress['video_id'])
        
        video_ids = [video_id for video_id in video_ids if video_id not in progress_video_ids]
        
        df = pd.concat([df, progress])
        
    # Collect our data, Added TQDM progress bar
    for i in tqdm(range(len(video_ids))):

        try:
            video_id = video_ids[i]

            if video_id is None:
                logging.info("Skipped NoneType video_id")
                continue

            logging.info("Downloading " + video_id)

            downloader.setVideoId(video_id)

            videoMetaData = downloader.getVideoMetadata()
            time.sleep(random.randint(1, 5))
            videoTranscript = downloader.getVideoTranscript()

            video = {
                "video_id": video_id,
                "title": videoMetaData["title"],
                "description": videoMetaData["description"],
                "tags": videoMetaData["tags"],
                "raw_duration": videoMetaData["raw_duration"],
                "duration": videoMetaData["duration"],
                "cleaned_transcript": videoTranscript["cleaned_transcript"],
                "raw_transcript": videoTranscript["raw_transcript"], 
                "link": "www.youtube.com/watch?v=" + video_id,
            }

            videos.append(video)

            logging.info("Finished downloading " + video_id)
        except Exception as e:
            # If we run into any error
            print(f"Ran into exception, saving progress and stopping.")
            logging.info(f"Ran into exception saving progress and stopping.")

            print(f"Exception: {e}")
            logging.info(f"Exception: {e}")

            df = pd.concat([df, pd.DataFrame(videos)])

            df.to_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + 'progress_' + save_path, index_label=False)

            print("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + 'progress_' + save_path))
            logging.info("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + 'progress_' + save_path))

            return df

    # If we complete the download.
    print("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(len(targets), time.time() - start))

    df = pd.concat([df, pd.DataFrame(videos)])

    df.to_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path, index_label=False)

    print("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path))
    logging.info("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path))

    return df

def classify_audit_results():
    '''
    Run classification, with a bit of options.
    '''
    single_classification = input("Would you like to run a single classification, as opposed to multiple? Y or N ").lower()

    print("Starting classification for downloaded audit videos.")
    logging.info("Starting classification for downloaded audit videos.")
    classify_paths = os.listdir(audit.AUDIT_SNIPPET_RESULTS_PATH)
    classify_paths = [path for path in classify_paths if 'homepage' in path or 'sidebar' in path]
    classify_paths = [path for path in classify_paths if 'snippets' in path]
    
    for path in classify_paths:
        data = pd.read_csv(audit.AUDIT_SNIPPET_RESULTS_PATH + path)
        split_path = path.strip('.csv').split("_")
        save_path = split_path[1] + "_" + split_path[2] + "_" + split_path[3] + "_predictions"

        print(f"Loaded data and starting classification for {save_path}")
        logging.info(f"Loaded data and starting classification for {save_path}")

        # For single runs or repeat runs, we can skip over classifications we have already made.
        if f"{save_path}.csv" in os.listdir(classifier.RESULTS_PATH):
            print("Already run classifications for this file.")
            logging.info("Already run classifications for this file.")

            run_again = input("Would you like to run classifications again? Y or N ").lower()
            if run_again == 'n':
                continue

        model = ChatCompletionModel(data, save_path = save_path)
        model.classify()

        print(f"Classification finished for {save_path} and saved to {classifier.RESULTS_PATH + save_path}.csv")
        logging.info(f"Classification finished for {save_path} and saved to {classifier.RESULTS_PATH + save_path}.csv")

        if single_classification == 'y':
            print(f"Completed single classification run.")
            logging.info(f"Completed single classification run.")
            break

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

        print("Creating snippets and saving to seed videos.")
        logging.info("Creating snippets and saving to seed videos.")
        createSnippets(youtube.INTERIM_SEED_DATA, youtube.SEED_VIDEOS + 'seed_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
        createSnippets(youtube.INTERIM_YOUNG_DATA, youtube.SEED_VIDEOS + 'young_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
        createSnippets(youtube.INTERIM_OLD_DATA, youtube.SEED_VIDEOS + 'old_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)


        print("Assessing GPT-3 accuracy on test seed videos")
        logging.info("Assessing GPT-3 accuracy on test seed videos")
        ### Add abiltiy to switch between fine tuned, binary, and baseline GPT classifier

        print("Running audit, please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit, please ensure you've logged into the account you're auditing with.")
        conduct_audit(audit.AUDITS)
        
    if 'seed' in targets:
        download_seed = input("Would you like to download the seed data: Y or N ").lower()
        download_age = input("Would you like to download the age data: Y or N ").lower()
        create_snippets = input("Would you like to create the snippets: Y or N ").lower()

        if download_seed == 'y':
            print("Downloading seed data")
            logging.info("Downloading seed data")
            downloadYoutubeData(youtube.RAW_SEED_DATA)

        if download_age == 'y':
            print("Creating and seperating age bucket videos.")
            logging.info("Creating and seperating age bucket videos.")
            processAgeVideos(youtube.RAW_AGE_DATA)

        if create_snippets == 'y':
            print("Creating snippets and saving to seed videos.")
            logging.info("Creating snippets and saving to seed videos.")
            createSnippets(youtube.INTERIM_SEED_DATA, youtube.SEED_VIDEOS + 'seed_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
            createSnippets(youtube.INTERIM_YOUNG_DATA, youtube.SEED_VIDEOS + 'young_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
            createSnippets(youtube.INTERIM_OLD_DATA, youtube.SEED_VIDEOS + 'old_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)


    if 'audit' in targets:
        print("Running audit, please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit, please ensure you've logged into the account you're auditing with.")

        single_audit = input("Would you like to run a single audit? Y or N ").lower()

        if single_audit == 'y':
            conduct_audit()
        else:
            conduct_audit(audit.AUDITS)

    if 'download-audit' in targets:
        print("Downloading audit data.")
        logging.info("Downloading audit data.")

        homepage = input("Would you like to download homepage videos? Y or N ").lower()
        sidebar = input("Would you like to download sidebar videos? Y or N ").lower()

        if homepage == 'y':
            for path in audit.HOMEPAGE_RESULTS_PATHS:

                print(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")
                logging.info(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")

                df = pd.read_csv(audit.AUDIT_RESULTS_PATH + path)
                df['video_id'] = df['url'].apply(extract_video_id)

                split_path = path.split('-')
                save_path = 'downloaded_homepage_' + split_path[1] + '_' + split_path[2] + '.csv'

                download_audit_videos(list(df['video_id']), save_path, 'homepage')

        if sidebar == 'y':
            for path in audit.SIDEBAR_RESULTS_PATHS:

                print(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")
                logging.info(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")

                df = pd.read_csv(audit.AUDIT_RESULTS_PATH + path)
                df['video_id'] = df['url'].apply(extract_video_id)

                split_path = path.split('-')
                save_path = 'downloaded_sidebar_' + split_path[1] + '_' + split_path[2] + '.csv'

                download_audit_videos(list(df['video_id']), save_path, 'sidebar')

    if 'create_audit_snippets' in targets:

        paths = os.listdir(audit.AUDIT_DOWNLOADED_RESULTS_PATH)
        paths = [path for path in paths if 'homepage' in path or 'sidebar' in path]

        for path in paths:
            print(f"Creating snippets for {audit.AUDIT_DOWNLOADED_RESULTS_PATH + path}")
            logging.info(f"Creating snippets for {audit.AUDIT_DOWNLOADED_RESULTS_PATH + path}")

            # Load CSV and remove videos with extreme durations.
            df = pd.read_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + path)

            df.loc[df[df['duration'] > str(datetime.time(hour = 1, minute = 0, second = 0))].index, "cleaned_transcript"] = " "
            print("Removed long duration videos.")
            logging.info("Removed long duration videos.")

            df.to_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + path, index_label = False)
            print("Saved updated videos.")
            logging.info("Saved updated videos.")
            
            createSnippets(audit.AUDIT_DOWNLOADED_RESULTS_PATH + path, audit.AUDIT_SNIPPET_RESULTS_PATH + path.strip(".csv") + "_with_snippets.csv", max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)

    if 'classify' in targets:
        classify_audit_results()

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
    print("END OF BUILD.\n")
    logging.info('END OF BUILD.\n')