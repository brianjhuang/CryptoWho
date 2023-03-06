#!/usr/bin/python
import os


class Audit(object):
    """
    Static class that includes configuration for our Audit process
    """

    # AUDIT VARIABLES
    USER_AGE = "young"  #'young' or 'old'
    FINANCE_VIDEO_TYPE = "blockchain"  #'traditional', 'blockchain', 'mixed'

    BROWSER = "firefox"  #'chrome', 'firefox'

    WATCH_BY_RATIO = True  # If True, watch videos by ratio of video duration, else watch by number of seconds
    WATCH_DURATION = 1  # Number of seconds to watch each video
    WATCH_RATIO = 0.5  # Ratio of video duration to watch

    NUM_RECOMMENDATIONS = (
        10  # Number of recommendations to collect, very large values may throw errors
    )

    YOUNG_SEED_AGE_VIDEO_PATH = "data/seed/youtube/young_videos.csv"
    OLD_SEED_AGE_VIDEO_PATH = "data/seed/youtube/old_videos.csv"
    SEED_FINANCE_VIDEO_PATH = "data/seed/youtube/seed_videos.csv"

    VIDEO_ID_COLUMN = "video_id"

    AUDIT_RESULTS_PATH = "data/audit/youtube/raw/"
    AUDIT_DOWNLOADED_RESULTS_PATH = "data/audit/youtube/processed/"

    AUDITS = [
        {"type": "traditional", "age": "young"},
        {"type": "mixed", "age": "young"},
        {"type": "blockchain", "age": "young"},
        {"type": "traditional", "age": "old"},
        {"type": "mixed", "age": "old"},
        {"type": "blockchain", "age": "old"},
    ]
