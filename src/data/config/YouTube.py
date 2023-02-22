#!/usr/bin/python
import os

class YouTube(object):
    """
    Static class that includes configuration for our YouTube Data Downloader
    """

    # General Config
    DOWNLOAD_SNIPPET = True
    DOWNLOAD_VIDEO_TAGS = True
    DOWNLOAD_VIDEO_TRANSCRIPT = True
    DOWNLOAD_VIDEO_COMMENTS = True

    #LOAD PATHS
    TEST_DATA = 'test/youtube/video_ids.csv'
    RAW_DATA = 'data/raw/youtube/seed_finance_videos.csv'

    # SAVE PATHS
    SEED_VIDEOS = 'data/seed/youtube/'
    AUDIT_VIDEOS = 'data/audit/youtube/'
    EXTERNAL_VIDEOS ='data/external/youtube/'
    LOGS_PATH = 'logs/youtube_downloads'

    # YouTube Data API Config
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    # Used by default when an API Key is not provided to the YouTubeVideoDownloader class
    YOUTUBE_DATA_API_KEY = os.environ.get('YOUTUBE_DATA_API_KEY')

    # Set the Number of Comments
    LIMIT_PAGES_COMMENTS = 1  # 200 Comments per page

    # # Recommended Videos
    # RETRIEVE_RECOMMENDED_VIDEOS = False
    # RECOMMENDED_VIDEOS_THRESHOLD = 10