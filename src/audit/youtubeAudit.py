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

from config import audit, test_config
from src.audit.utils import get_full_url
from src.audit.YTDriver import YTDriver
import datetime


def get_age_seed_videos(user_age = audit.USER_AGE, test = False):

    if test:
        if user_age == "young":
            df = pd.read_csv(test_config.YOUNG_SEED_AGE_VIDEO_PATH)
        elif user_age == "old":
            df = pd.read_csv(test_config.OLD_SEED_AGE_VIDEO_PATH)
        else:
            raise ValueError('User age must be "young" or "old"')
    else:
        if user_age == "young":
            df = pd.read_csv(audit.YOUNG_SEED_AGE_VIDEO_PATH)
        elif user_age == "old":
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

    video_ids = df[audit.VIDEO_ID_COLUMN].values
    video_urls = [get_full_url(video_id) for video_id in video_ids]
    return video_urls, durations


def get_finance_seed_videos(finance_video_type = audit.FINANCE_VIDEO_TYPE, test = False):
    if test:
        df = pd.read_csv(test_config.SEED_FINANCE_VIDEO_PATH)
    else:
        df = pd.read_csv(test_config.SEED_FINANCE_VIDEO_PATH)
    df["label"] = df["label"].apply(str.lower)

    if finance_video_type == "mixed":
        # Grab half of the videos from both labels, sort by duration so we have the shortest videos
        traditional = df[df["label"] == "traditional"].sort_values(by="duration")[
            : len(df[df["label"] == "traditional"]) // 2
        ]

        blockchain = df[df["label"] == "blockchain"].sort_values(by="duration")[
            : len(df[df["label"] == "blockchain"]) // 2
        ]

        df = pd.concat([traditional, blockchain]).reset_index(drop=True)
    else:
        df = df[df["label"] == finance_video_type]

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


def process_durations_list(durations, test = False):
    if test:
        if test_config.WATCH_BY_RATIO:
            durations = [int(duration * test_config.WATCH_RATIO) for duration in durations]
        else:
            durations = [audit.WATCH_DURATION for duration in durations]
    else:
        if audit.WATCH_BY_RATIO:
            durations = [int(duration * audit.WATCH_RATIO) for duration in durations]
        else:
            durations = [audit.WATCH_DURATION for duration in durations]

    return durations


def to_csv(driver, start_time, finance_video_type = audit.FINANCE_VIDEO_TYPE, user_age = audit.USER_AGE, test = False):
    start_time_str = str(start_time).replace(
        ".", ""
    )  # Remove period from start time for filenames

    video_recs_df = pd.DataFrame(driver.video_recs)
    video_recs_df["Start Time"] = start_time
    video_recs_df["Age"] = audit.USER_AGE
    video_recs_df["Finance Video Type"] = finance_video_type

    homepage_recs_df = pd.DataFrame(driver.homepage_recs)
    homepage_recs_df["Start Time"] = start_time
    homepage_recs_df["Age"] = audit.USER_AGE
    homepage_recs_df["Finance Video Type"] = finance_video_type

    if test:
        if test_config.WATCH_BY_RATIO:
            video_recs_df.to_csv(
                test_config.AUDIT_RESULTS_PATH
                + f"test-{start_time_str}-{finance_video_type}-{user_age}-watch_ratio{test_config.WATCH_RATIO}-video_recs.csv",
                index=False,
            )

            homepage_recs_df.to_csv(
                test_config.AUDIT_RESULTS_PATH
                + f"test-{start_time_str}-{finance_video_type}-{user_age}-watch_ratio{test_config.WATCH_RATIO}-homepage_recs.csv",
                index=False,
            )

        else:
            video_recs_df.to_csv(
                test_config.AUDIT_RESULTS_PATH
                + f"test-{start_time_str}-{finance_video_type}-{user_age}-watch_time{test_config.WATCH_DURATION}-video_recs.csv",
                index=False,
            )

            homepage_recs_df.to_csv(
                test_config.AUDIT_RESULTS_PATH
                + f"test-{start_time_str}-{finance_video_type}-{user_age}-watch_time{test_config.WATCH_DURATION}-homepage_recs.csv",
                index=False,
            )

        if driver.errors:
            if audit.WATCH_BY_RATIO:
                errors_df = pd.DataFrame(driver.errors)
                errors_df.to_csv(
                    audit.AUDIT_RESULTS_PATH
                    + f"test-{start_time_str}-{finance_video_type}-{user_age}-errors.csv",
                    index=False,
                )
            else:
                errors_df = pd.DataFrame(driver.errors)
                errors_df.to_csv(
                    audit.AUDIT_RESULTS_PATH
                    + f"test-{start_time_str}-{finance_video_type}-{user_age}-watch_time{audit.WATCH_DURATION}-errors.csv",
                    index=False,
                )
    else:
        if audit.WATCH_BY_RATIO:
            video_recs_df.to_csv(
                audit.AUDIT_RESULTS_PATH
                + f"{start_time_str}-{finance_video_type}-{user_age}-watch_ratio{audit.WATCH_RATIO}-video_recs.csv",
                index=False,
            )

            homepage_recs_df.to_csv(
                audit.AUDIT_RESULTS_PATH
                + f"{start_time_str}-{finance_video_type}-{user_age}-watch_ratio{audit.WATCH_RATIO}-homepage_recs.csv",
                index=False,
            )

        else:
            video_recs_df.to_csv(
                audit.AUDIT_RESULTS_PATH
                + f"{start_time_str}-{finance_video_type}-{user_age}-watch_time{audit.WATCH_DURATION}-video_recs.csv",
                index=False,
            )

            homepage_recs_df.to_csv(
                audit.AUDIT_RESULTS_PATH
                + f"{start_time_str}-{finance_video_type}-{user_age}-watch_time{audit.WATCH_DURATION}-homepage_recs.csv",
                index=False,
            )

        if driver.errors:
            if audit.WATCH_BY_RATIO:
                errors_df = pd.DataFrame(driver.errors)
                errors_df.to_csv(
                    audit.AUDIT_RESULTS_PATH
                    + f"{start_time_str}-{finance_video_type}-{user_age}-errors.csv",
                    index=False,
                )
            else:
                errors_df = pd.DataFrame(driver.errors)
                errors_df.to_csv(
                    audit.AUDIT_RESULTS_PATH
                    + f"{start_time_str}-{finance_video_type}-{user_age}-watch_time{audit.WATCH_DURATION}-errors.csv",
                    index=False,
                )

def run_audit(finance_video_type = audit.FINANCE_VIDEO_TYPE, user_age = audit.USER_AGE, test = False):
    if test:
        # Record start time
        start_time = time.time()
        driver = YTDriver(browser=audit.BROWSER, verbose=True)

        print(f"Starting test {user_age} {finance_video_type} audit")

        # Watch age seed videos
        print("Watching age videos...")
        age_seed_videos, age_seed_video_durations = get_age_seed_videos(user_age, test = test)
        age_seed_video_durations = process_durations_list(age_seed_video_durations, test = test)
        driver.play_list(
            age_seed_videos,
            age_seed_video_durations,
            homepage_interval=0,
            topn=audit.NUM_RECOMMENDATIONS,
        )

        to_csv(driver, start_time, finance_video_type, user_age, test = True)

        # Watch finance videos
        print("Watching finance videos...")
        finance_seed_videos, finance_seed_video_durations = get_finance_seed_videos(finance_video_type, test = test)
        finance_seed_video_durations = process_durations_list(finance_seed_video_durations, test = test)
        driver.play_list(
            finance_seed_videos,
            finance_seed_video_durations,
            homepage_interval=10,
            topn=audit.NUM_RECOMMENDATIONS,
        )

        driver.close()  # Only closes the browser, object and results are still available

        # Save results to csv
        to_csv(driver, start_time, finance_video_type, user_age, test = True)

    else:
        # Record start time
        start_time = time.time()
        driver = YTDriver(browser=audit.BROWSER, verbose=True)

        print(f"Starting {user_age} {finance_video_type} audit")

        # Watch age seed videos
        print("Watching age videos...")
        age_seed_videos, age_seed_video_durations = get_age_seed_videos(user_age)
        age_seed_video_durations = process_durations_list(age_seed_video_durations)
        driver.play_list(
            age_seed_videos,
            age_seed_video_durations,
            homepage_interval=0,
            topn=audit.NUM_RECOMMENDATIONS,
        )

        to_csv(driver, start_time, finance_video_type, user_age)

        # Watch finance videos
        print("Watching finance videos...")
        finance_seed_videos, finance_seed_video_durations = get_finance_seed_videos(finance_video_type)
        finance_seed_video_durations = process_durations_list(finance_seed_video_durations)
        driver.play_list(
            finance_seed_videos,
            finance_seed_video_durations,
            homepage_interval=10,
            topn=audit.NUM_RECOMMENDATIONS,
        )

        driver.close()  # Only closes the browser, object and results are still available

        # Save results to csv
        to_csv(driver, start_time, finance_video_type, user_age)
