#!/usr/bin/python
import os


class Audit(object):
    """
    Static class that includes configuration for our Audit process
    """

    #AUDIT VARIABLES
    USER_AGE = 'young' #'young' or 'old'
    FINANCE_VIDEO_TYPE = 'traditional' #'traditional', 'blockchain', 'mixed', 'unrelated'

    WATCH_DURATION = 10 #Number of seconds to watch each video
    NUM_RECOMMENDATIONS = 10 #Number of recommendations to collect, very large values may throw errors

    #PATH VARIABLES
    SEED_AGE_VIDEO_PATH = 'data/raw/youtube/seed_age_videos.csv'
    SEED_FINANCE_VIDEO_PATH = 'data/raw/youtube/seed_finance_videos.csv'

    AUDIT_RESULTS_PATH = 'data/audit/youtube/'