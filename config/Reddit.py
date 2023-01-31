#!/usr/bin/python
import os

class Reddit(object):
    """
    Static class that includes configuration for our Reddit Data Scraper
    """

    # GENERAL CONFIG
    SUBREDDITS = ['investing', 'finance', 'cryptocurrency', 'wallstreetbets']
    

    # SAVE PATHS
    RAW_VIDEOS = '../../data/raw/reddit/'
    PROCESSED_VIDEOS = '../../data/processed/reddit/'
    INTERIM_VIDEOS = '../../data/interim/reddit/'
    EXTERNAL_VIDEOS ='../../data/external/reddit/'