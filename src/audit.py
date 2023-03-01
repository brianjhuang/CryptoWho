import sys
sys.path.insert(0, '..')
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
import sys
import pandas as pd
import re
import time

from config import audit
from src.utils import get_full_url
from src.YTDriver import YTDriver

def get_age_seed_videos():
    df = pd.read_csv(audit.SEED_AGE_VIDEO_PATH, index_col=0)
    df = df[df['label'] == audit.USER_AGE]
    video_ids = df['video_id'].values
    video_urls = [get_full_url(video_id) for video_id in video_ids]
    return video_urls

def get_finance_seed_videos():
    df = pd.read_csv(audit.SEED_FINANCE_VIDEO_PATH, index_col=0)
    df = df[df['label'] == audit.FINANCE_VIDEO_TYPE]
    video_ids = df['video_id'].values
    video_urls = [get_full_url(video_id) for video_id in video_ids]
    return video_urls

def to_csv(driver, start_time):
    start_time_str = str(start_time).replace('.', '') #Remove period from start time for filenames

    video_recs_df = pd.DataFrame(driver.video_recs)
    video_recs_df['Start Time'] = start_time
    video_recs_df['Age'] = audit.USER_AGE
    video_recs_df['Finance Video Type'] = audit.FINANCE_VIDEO_TYPE
    video_recs_df.to_csv(audit.AUDIT_RESULTS_PATH + f'{start_time_str}-video_recs.csv', index=False)

    homepage_recs_df = pd.DataFrame(driver.homepage_recs)
    homepage_recs_df['Start Time'] = start_time
    homepage_recs_df['Age'] = audit.USER_AGE
    homepage_recs_df['Finance Video Type'] = audit.FINANCE_VIDEO_TYPE
    homepage_recs_df.to_csv(audit.AUDIT_RESULTS_PATH + f'{start_time_str}-homepage_recs.csv', index=False)

def run_audit():

    #Record start time
    start_time = time.time()
    driver = YTDriver(browser='firefox', verbose=True)

    #Watch age seed videos
    age_seed_videos = get_age_seed_videos()
    driver.play_list(age_seed_videos[5:7], duration = audit.WATCH_DURATION, homepage_interval=0)

    #Watch finance videos
    finance_seed_videos = get_finance_seed_videos()
    driver.play_list(finance_seed_videos[5:7], duration = audit.WATCH_DURATION, homepage_interval=10)

    driver.close() #Only closes the browser, object and results are still available

    #Save results to csv
    to_csv(driver, start_time)
