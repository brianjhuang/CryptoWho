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
    RAW_THREADS = '../../data/raw/reddit/'
    PROCESSED_THREADS = '../../data/processed/reddit/'
    INTERIM_THREADS = '../../data/interim/reddit/'
    EXTERNAL_THREADS ='../../data/external/reddit/'