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

    # SAVE PATHS
    RAW_VIDEOS = 'data/raw/youtube/'
    PROCESSED_VIDEOS = 'data/processed/youtube/'
    INTERIM_VIDEOS = 'data/interim/youtube/'
    EXTERNAL_VIDEOS ='data/external/youtube/'

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