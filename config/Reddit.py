#!/usr/bin/python
import os

class Reddit(object):
    """
    Static class that includes configuration for our Reddit Data Scraper
    """

    # GENERAL CONFIG
    SUBREDDITS = ['investing', 'finance', 'cryptocurrency', 'wallstreetbets']
    SCRAPE_DEPTH = 2 # How many pages to scrape per subreddit (25 threads per page)

    # SAVE PATHS
    RAW_VIDEOS = '../../data/raw/reddit/'
    PROCESSED_VIDEOS = '../../data/processed/reddit/'
    INTERIM_VIDEOS = '../../data/interim/reddit/'
    EXTERNAL_VIDEOS ='../../data/external/reddit/'