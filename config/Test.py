#!/usr/bin/python
import os

class Test(object):
    """
    Static class that includes configuration for our Test target
    """

    #PATHS (DOWNLOAD)
    RAW_SEED_DATA = 'test/youtube/test_seed_finance_videos.csv'
    RAW_AGE_DATA = 'test/youtube/test_seed_age_videos.csv'
    INTERIM_SEED_DATA = 'data/interim/youtube/test_seed_videos.csv'
    INTERIM_YOUNG_DATA = 'data/interim/youtube/test_young_videos.csv'
    INTERIM_OLD_DATA = 'data/interim/youtube/test_old_videos.csv'

    #PATHS (CLASSIFIER)

    # SAVE PATHS
    SEED_RESULTS_PATH = 'test_seed_predictions'
    CONFUSION_MATRIX_PATH = 'references/figures/test_seed_training_results.png'

    # LOAD PATHS
    SEED_LOAD_PATHS = ['data/seed/youtube/test_seed_videos.csv', 'data/seed/youtube/test_young_videos.csv', 'data/seed/youtube/test_old_videos.csv']

    #PATHS (AUDIT)
    YOUNG_SEED_AGE_VIDEO_PATH = "data/seed/youtube/test_young_videos.csv"
    OLD_SEED_AGE_VIDEO_PATH = "data/seed/youtube/test_old_videos.csv"
    SEED_FINANCE_VIDEO_PATH = "data/seed/youtube/test_seed_videos.csv"

    AUDIT_RESULTS_PATH = "data/audit/youtube/raw/"
    AUDIT_DOWNLOADED_RESULTS_PATH = "data/audit/youtube/processed/"
    AUDIT_SNIPPET_RESULTS_PATH = "data/audit/youtube/processed/snippets/"

    results = os.listdir('data/audit/youtube/raw')
    TEMP_HOMEPAGE_RESULTS = [result for result in results if 'homepage' in result]
    TEMP_SIDEBAR_RESULTS = [result for result in results if 'video_recs' in result]
    HOMEPAGE_RESULTS_PATHS = [result for result in TEMP_HOMEPAGE_RESULTS if 'test' in result]
    SIDEBAR_RESULTS_PATHS = [result for result in TEMP_SIDEBAR_RESULTS if 'test' in result]

    #CONFIG (AUDIT)
    WATCH_BY_RATIO = False  # If True, watch videos by ratio of video duration, else watch by number of seconds
    WATCH_DURATION = 5  # Number of seconds to watch each video
    WATCH_RATIO = 0.01  # Ratio of video duration to watch