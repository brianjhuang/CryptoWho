import json
import pandas as pd
import os
import subprocess
import re

def json_to_csv(data, filepath):
    df = pd.DataFrame(data)
    if not os.path.isfile(filepath): # If file doesn't exist yet
        df.to_csv(filepath, index=False)
    else: # Only append if file already exists
        df.to_csv(filepath, mode='a', header=False, index=False)
        
def json_to_parquet(data, filepath):
    df = pd.DataFrame(data)
    if not os.path.isfile(filepath): # If file doesn't exist yet
        df.to_parquet(filepath, engine='fastparquet', index=False)
    else: # Only append if file already exists
        df.to_parquet(filepath, engine='fastparquet', append=True, index=False)
        
def list_to_csv(data, filepath):
    df = pd.DataFrame(data, columns=['url'])
    if not os.path.isfile(filepath): # If file doesn't exist yet
        df.to_csv(filepath, index=False)        
    else: # Only append if file already exists
        df.to_csv(filepath, mode='a', header=False, index=False)

def get_data(filepath):
    return pd.read_csv(filepath)

def get_video_id(url):
    return re.search(r'[?&]v=(.*)?$', url).group(1).split('&')[0]

def get_full_url(videoId):
    return f'https://www.youtube.com/watch?v={videoId}'

### These helper functions/data strctures come from code associated with the
### original paper, published by the authors:
### https://github.com/ucdavis-noyce/YouTube-Driver
def time2seconds(s):
    """
    Converts a given time (video duration, ad time, etc.) to seconds
    """
    s = s.split(':')
    s.reverse()
    wait = 0
    factor = 1
    for t in s:
        wait += int(t) * factor
        factor *= 60
    return wait



class Video:
    def __init__(self, elem, url):
        self.elem = elem
        self.url = url
        self.videoId = re.search(r'[?&]v=(.*)?$', url).group(1).split('&')[0]
        self.metadata = None

    def get_metadata(self):
        """
        Get video metadata using `youtube-dl`.
        """
        if self.metadata is None:
            proc = subprocess.run(['youtube-dl', '-J', self.url], stdout=subprocess.PIPE)
            self.metadata = json.loads(proc.stdout.decode())
        return self.metadata


class VideoUnavailableException(Exception):
    """
    Exception thrown when a played video is private/deleted/copyright struck.
    """
    pass