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
import numpy as np
import matplotlib.pyplot as plt   
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import random
import re
import math

from src.data.youtubeDownloader import Downloader
from src.features.youtubeCleaner import Cleaner
from src.audit.youtubeAudit import run_audit
from src.model.gpt import ChatCompletionModel
from config import youtube, audit, classifier, test_config

# Logging variables
totalLogs = len(os.listdir('logs'))
logFileName = 'logs/log_{0}.txt'.format(totalLogs)


# Set up the settings to log information as we run our build pipeline
logging.basicConfig(filename=logFileName, 
        filemode='a', 
        level=logging.INFO,
        datefmt='%H:%M:%S',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

# Cost per GPT call
TURBO_COST = 0.00200 / 1000

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
        df[df['label'] == 'young'].to_csv(youtube.INTERIM_VIDEOS + 'test_young_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_young_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_young_videos.csv'))

        df[df['label'] == 'old'].to_csv(youtube.INTERIM_VIDEOS + 'test_old_videos.csv', index_label=False)

        print("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_old_videos.csv'))
        logging.info("Saved file to:  {0}".format(youtube.INTERIM_VIDEOS + 'test_old_videos.csv'))
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

def make_confusion_matrix(cf,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=None,
                          cmap='Blues',
                          title=None):
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.
    Arguments
    ---------
    cf:            confusion matrix to be passed in
    group_names:   List of strings that represent the labels row by row to be shown in each square.
    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'
    count:         If True, show the raw number in the confusion matrix. Default is True.
    normalize:     If True, show the proportions for each category. Default is True.
    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.
    xyticks:       If True, show x and y ticks. Default is True.
    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.
    sum_stats:     If True, display summary statistics below the figure. Default is True.
    figsize:       Tuple representing the figure size. Default will be the matplotlib rcParams value.
    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html
                   
    title:         Title for the heatmap. Default is None.
    '''


    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names)==cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = ["{0:.2%}".format(value) for value in cf.flatten()/np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0],cf.shape[1])


    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        #Accuracy is sum of diagonal divided by total observations
        accuracy  = np.trace(cf) / float(np.sum(cf)) * 100

        #if it is a binary confusion matrix, show some more stats
        if len(cf)==2:
            #Metrics for Binary Confusion Matrices
            precision = cf[1,1] / sum(cf[:,1])
            recall    = cf[1,1] / sum(cf[1,:])
            f1_score  = 2*precision*recall / (precision + recall)
            stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
                accuracy,precision,recall,f1_score)
        else:
            stats_text = "\n\nAccuracy={:0.3f}%".format(accuracy)
    else:
        stats_text = ""


    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if figsize==None:
        #Get default figure size if not set
        figsize = plt.rcParams.get('figure.figsize')

    if xyticks==False:
        #Do not show categories if xyticks is False
        categories=False


    # MAKE THE HEATMAP VISUALIZATION
    plt.figure(figsize=figsize)
    output = sns.heatmap(cf,annot=box_labels,fmt="",cmap=cmap,cbar=cbar,xticklabels=categories,yticklabels=categories)

    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)
    
    if title:
        plt.title(title)

    return output

def classify_seed(load_paths, save_path, viz_path):
    """Runs classifier on seed videos."""

    print("Starting classification for downloaded seed videos.")
    logging.info("Starting classification for downloaded seed videos.")

    # Load all the seed videos
    data = pd.DataFrame()

    for path in load_paths:
        data = pd.concat([data, pd.read_csv(path)])

    data['label'] = data['label'].apply(lambda x: 'Unrelated' if x == 'old' else 'Unrelated' if x == 'young' else 'Unrelated' if x == 'None' else x)

    print(f"Loaded data and starting classification for {save_path}")
    logging.info(f"Loaded data and starting classification for {save_path}")

    model = ChatCompletionModel(data, save_path = save_path)
    predictions = model.classify()

    print(f"Classification finished for {save_path} and saved to {save_path}.csv")
    logging.info(f"Classification finished for {save_path} and saved to {save_path}.csv")

    preds = list(predictions['prediction'])
    actual = list(data['label'])

    # Deal with this later where classifications return 'Label: Prediction'
    preds = ['Unrelated' if pred == 'Label' else pred for pred in preds]
    total_cost = sum(predictions['total_tokens']) * TURBO_COST

    report = classification_report(actual, preds)

    print(f"Classification Report: \n")
    logging.info(f"Classification Report: \n")

    print(report)
    logging.info(report)

    print(f"Total Cost: {total_cost}")
    logging.info(f"Total cost: {total_cost}")

    labels = ['Blockchain', 'Mixed', 'Traditional', 'Unrelated']
    cf_matrix = confusion_matrix(actual, preds)

    make_confusion_matrix(cf_matrix, categories = labels, cmap = "rocket").get_figure().savefig(viz_path, dpi = 300, bbox_inches ='tight')

    print(f"Visulization generated and saved to {viz_path}")
    logging.info(f"Visualization generated and saved to {viz_path}")
    

def conduct_audit(audits = [], test = False):
    """Run the audit"""
    if test:
        for run in audits:
            run_audit(run['type'], run['age'], test = test)
            time.sleep(5)
    else:
        if len(audits) <= 0:
            run_audit()
        else:
            for run in audits:
                run_audit(run['type'], run['age'])
                time.sleep(600)

def download_audit_videos(video_ids, save_path, kind):
    """Download our videos from the audit"""       
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
    print("Downloaded {0} in {1} seconds.".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path, time.time() - start))
    logging.info("Downloaded {0} in {1} seconds.".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path, time.time() - start))

    df = pd.concat([df, pd.DataFrame(videos)])

    df.to_csv(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path, index_label=False)

    print("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path))
    logging.info("Saved file to:  {0}".format(audit.AUDIT_DOWNLOADED_RESULTS_PATH + save_path))

    return df

def classify_audit_results(test = False):
    '''
    Run classification, with a bit of options.
    '''
    single_classification = input("Would you like to run a single classification, as opposed to multiple? Y or N ").lower()

    print("Starting classification for downloaded audit videos.")
    logging.info("Starting classification for downloaded audit videos.")
    if test:
        classify_paths = os.listdir(audit.AUDIT_SNIPPET_RESULTS_PATH)
        classify_paths = [path for path in classify_paths if 'homepage' in path or 'sidebar' in path]
        classify_paths = [path for path in classify_paths if 'snippets' in path]
        classify_paths = [path for path in classify_paths if 'test' in path]
    else:
        classify_paths = os.listdir(audit.AUDIT_SNIPPET_RESULTS_PATH)
        classify_paths = [path for path in classify_paths if 'homepage' in path or 'sidebar' in path]
        classify_paths = [path for path in classify_paths if 'snippets' in path]
    
    for path in classify_paths:
        data = pd.read_csv(audit.AUDIT_SNIPPET_RESULTS_PATH + path)
        split_path = path.strip('.csv').split("_")

        if test:
            save_path = 'test_' + split_path[2] + "_" + split_path[3] + "_" + split_path[4] + "_predictions"
        else:
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

    if 'classify-seed' in targets:
        classify_seed(classifier.SEED_LOAD_PATHS, classifier.SEED_RESULTS_PATH, classifier.CONFUSION_MATRIX_PATH)

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

    if 'create-audit-snippets' in targets:

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
        classify_seed(classifier.SEED_LOAD_PATHS, classifier.SEED_RESULTS_PATH, classifier.CONFUSION_MATRIX_PATH)

        print("Running audit(s), please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit(s), please ensure you've logged into the account you're auditing with.")
        conduct_audit(audit.AUDITS)

        print("Audits completed.")
        logging.info("Audits completed")
        time.sleep(5)

        print("Downloading audit data.")
        logging.info("Downloading audit data.")

        print("Downloading homepage data.")
        logging.info("Downloading homepage data.")
        for path in audit.HOMEPAGE_RESULTS_PATHS:
            print(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")
            logging.info(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")

            df = pd.read_csv(audit.AUDIT_RESULTS_PATH + path)
            df['video_id'] = df['url'].apply(extract_video_id)

            split_path = path.split('-')
            save_path = 'downloaded_homepage_' + split_path[1] + '_' + split_path[2] + '.csv'

            download_audit_videos(list(df['video_id']), save_path, 'homepage')


        print("Downloading sidebar data.")
        logging.info("Downloading sidebar data.")
        for path in audit.SIDEBAR_RESULTS_PATHS:
            print(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")
            logging.info(f"Downloading {audit.AUDIT_RESULTS_PATH + path}")

            df = pd.read_csv(audit.AUDIT_RESULTS_PATH + path)
            df['video_id'] = df['url'].apply(extract_video_id)

            split_path = path.split('-')
            save_path = 'downloaded_sidebar_' + split_path[1] + '_' + split_path[2] + '.csv'

            download_audit_videos(list(df['video_id']), save_path, 'sidebar')

        paths = os.listdir(audit.AUDIT_DOWNLOADED_RESULTS_PATH)
        paths = [path for path in paths if 'homepage' in path or 'sidebar' in path]

        print("Creating snippets.")
        logging.info("Creating snippets.")
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

        print("Running classification")
        logging.info("Running classification")
        classify_audit_results()

    if 'test' in targets:
        print("Running test pipeline")
        logging.info("Running test pipeline")
        
        print("Downloading seed data")
        logging.info("Downloading seed data")
        downloadYoutubeData(test_config.RAW_SEED_DATA, test = True)

        print("Creating and seperating age bucket videos.")
        logging.info("Creating and seperating age bucket videos.")
        processAgeVideos(test_config.RAW_AGE_DATA, test = True)

        print("Creating snippets and saving to seed videos.")
        logging.info("Creating snippets and saving to seed videos.")
        createSnippets(test_config.INTERIM_SEED_DATA, youtube.SEED_VIDEOS + 'test_seed_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
        createSnippets(test_config.INTERIM_YOUNG_DATA, youtube.SEED_VIDEOS + 'test_young_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)
        createSnippets(test_config.INTERIM_OLD_DATA, youtube.SEED_VIDEOS + 'test_old_videos.csv', max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)


        print("Assessing GPT-3 accuracy on test seed videos")
        logging.info("Assessing GPT-3 accuracy on test seed videos")
        classify_seed(test_config.SEED_LOAD_PATHS, test_config.SEED_RESULTS_PATH, test_config.CONFUSION_MATRIX_PATH)

        print("Running audit(s), please ensure you've logged into the account you're auditing with.")
        logging.info("Running audit(s), please ensure you've logged into the account you're auditing with.")
        conduct_audit(audit.AUDITS, test = True)

        print("Audits completed.")
        logging.info("Audits completed")
        time.sleep(5)

        print("Downloading audit data.")
        logging.info("Downloading audit data.")

        print("Downloading homepage data.")
        logging.info("Downloading homepage data.")

        for path in test_config.HOMEPAGE_RESULTS_PATHS:
            print(f"Downloading {test_config.AUDIT_RESULTS_PATH + path}")
            logging.info(f"Downloading {test_config.AUDIT_RESULTS_PATH + path}")

            df = pd.read_csv(test_config.AUDIT_RESULTS_PATH + path)
            df['video_id'] = df['url'].apply(extract_video_id)

            split_path = path.split('-')
            save_path = 'test_downloaded_homepage_' + split_path[2] + '_' + split_path[3] + '.csv'

            download_audit_videos(list(df['video_id']), save_path, 'homepage')


        print("Downloading sidebar data.")
        logging.info("Downloading sidebar data.")
        for path in test_config.SIDEBAR_RESULTS_PATHS:
            print(f"Downloading {test_config.AUDIT_RESULTS_PATH + path}")
            logging.info(f"Downloading {test_config.AUDIT_RESULTS_PATH + path}")

            df = pd.read_csv(test_config.AUDIT_RESULTS_PATH + path)
            df['video_id'] = df['url'].apply(extract_video_id)

            split_path = path.split('-')
            save_path = 'test_downloaded_sidebar_' + split_path[2] + '_' + split_path[3] + '.csv'

            download_audit_videos(list(df['video_id']), save_path, 'sidebar')

        paths = os.listdir(test_config.AUDIT_DOWNLOADED_RESULTS_PATH)

        paths = [path for path in paths if 'homepage' in path or 'sidebar' in path]
        paths = [path for path in paths if 'test' in path]

        print("Creating snippets.")
        logging.info("Creating snippets.")
        for path in paths:
            print(f"Creating snippets for {test_config.AUDIT_DOWNLOADED_RESULTS_PATH + path}")
            logging.info(f"Creating snippets for {test_config.AUDIT_DOWNLOADED_RESULTS_PATH + path}")

            # Load CSV and remove videos with extreme durations.
            df = pd.read_csv(test_config.AUDIT_DOWNLOADED_RESULTS_PATH + path)

            df.loc[df[df['duration'] > str(datetime.time(hour = 1, minute = 0, second = 0))].index, "cleaned_transcript"] = " "
            print("Removed long duration videos.")
            logging.info("Removed long duration videos.")

            df.to_csv(test_config.AUDIT_DOWNLOADED_RESULTS_PATH + path, index_label = False)
            print("Saved updated videos.")
            logging.info("Saved updated videos.")
            
            createSnippets(test_config.AUDIT_DOWNLOADED_RESULTS_PATH + path, test_config.AUDIT_SNIPPET_RESULTS_PATH + path.strip(".csv") + "_with_snippets.csv", max_word_count=youtube.MAX_WORD_COUNT, use_ratio=youtube.USE_RATIO, ratio = youtube.RATIO)

        print("Running classification")
        logging.info("Running classification")
        classify_audit_results(test = True)


if __name__ == '__main__':
    targets = [target.lower() for target in sys.argv[1:]]

    main(targets)
    print("END OF BUILD.\n")
    logging.info('END OF BUILD.\n')