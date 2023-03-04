import sys

sys.path.insert(0, "..")
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
import sys
import pandas as pd
import re
import time

from config import audit
from src.audit.utils import get_full_url
from src.audit.YTDriver import YTDriver
import datetime


def get_age_seed_videos():
    if audit.USER_AGE == "young":
        df = pd.read_csv(audit.YOUNG_SEED_AGE_VIDEO_PATH)
    elif audit.USER_AGE == "old":
        df = pd.read_csv(audit.OLD_SEED_AGE_VIDEO_PATH)
    else:
        raise ValueError('User age must be "young" or "old"')

    # Convert duration to seconds
    df["duration"] = df["duration"].apply(
        lambda x: datetime.datetime.strptime(x, "%H:%M:%S").time()
    )
    df["duration"] = df["duration"].apply(
        lambda x: x.hour * 3600 + x.minute * 60 + x.second
    )
    durations = df["duration"].values

    # df = df[df['label'] == audit.USER_AGE]
    video_ids = df[audit.VIDEO_ID_COLUMN].values
    video_urls = [get_full_url(video_id) for video_id in video_ids]
    return video_urls, durations


def get_finance_seed_videos():
    df = pd.read_csv(audit.SEED_FINANCE_VIDEO_PATH)

    if audit.FINANCE_VIDEO_TYPE == "mixed":
        # Grab half of the videos from both labels, sort by duration so we have the shortest videos
        traditional = df[df["label"].lower() == "traditional"].sort_values(
            by="duration"
        )[: len(df[df["label"].lower() == "traditional"]) // 2]
        
        blockchain = df[df["label"].lower() == "blockchain"].sort_values(by="duration")[
            : len(df[df["label"].lower() == "blockchain"]) // 2
        ]

        df = pd.concat(traditional, blockchain).reset_index(drop=True)
    else:
        df = df[df["label"] == audit.FINANCE_VIDEO_TYPE]

    # Convert duration to seconds
    df["duration"] = df["duration"].apply(
        lambda x: datetime.datetime.strptime(x, "%H:%M:%S").time()
    )
    df["duration"] = df["duration"].apply(
        lambda x: x.hour * 3600 + x.minute * 60 + x.second
    )
    durations = df["duration"].values

    video_ids = df[audit.VIDEO_ID_COLUMN].values
    video_urls = [get_full_url(video_id) for video_id in video_ids]
    return video_urls, durations


def process_durations_list(durations):
    if audit.WATCH_BY_RATIO:
        durations = [int(duration * audit.WATCH_RATIO) for duration in durations]
    else:
        durations = [audit.WATCH_DURATION for duration in durations]
    return durations


get_age_seed_videos()


def to_csv(driver, start_time):
    start_time_str = str(start_time).replace(
        ".", ""
    )  # Remove period from start time for filenames

    video_recs_df = pd.DataFrame(driver.video_recs)
    video_recs_df["Start Time"] = start_time
    video_recs_df["Age"] = audit.USER_AGE
    video_recs_df["Finance Video Type"] = audit.FINANCE_VIDEO_TYPE
    video_recs_df.to_csv(
        audit.AUDIT_RESULTS_PATH + f"{start_time_str}-video_recs.csv", index=False
    )

    homepage_recs_df = pd.DataFrame(driver.homepage_recs)
    homepage_recs_df["Start Time"] = start_time
    homepage_recs_df["Age"] = audit.USER_AGE
    homepage_recs_df["Finance Video Type"] = audit.FINANCE_VIDEO_TYPE
    homepage_recs_df.to_csv(
        audit.AUDIT_RESULTS_PATH + f"{start_time_str}-homepage_recs.csv", index=False
    )

    if driver.errors:
        errors_df = pd.DataFrame(driver.errors)
        errors_df.to_csv(
            audit.AUDIT_RESULTS_PATH + f"{start_time_str}-errors.csv", index=False
        )


def run_audit():
    # Record start time
    start_time = time.time()
    driver = YTDriver(browser="firefox", verbose=True)

    # Watch age seed videos
    age_seed_videos, age_seed_video_durations = get_age_seed_videos()
    age_seed_video_durations = process_durations_list(age_seed_video_durations)
    driver.play_list(
        age_seed_videos,
        age_seed_video_durations,
        homepage_interval=0,
        topn=audit.NUM_RECOMMENDATIONS,
    )
    to_csv(driver, start_time)

    # Watch finance videos
    finance_seed_videos, finance_seed_video_durations = get_finance_seed_videos()
    finance_seed_video_durations = process_durations_list(finance_seed_video_durations)
    driver.play_list(
        finance_seed_videos,
        finance_seed_video_durations,
        homepage_interval=10,
        topn=audit.NUM_RECOMMENDATIONS,
    )

    driver.close()  # Only closes the browser, object and results are still available

    # Save results to csv
    to_csv(driver, start_time)
