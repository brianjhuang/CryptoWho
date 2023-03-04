import pandas as pd
import numpy as np

import openai
import os
import sys
from tqdm import tqdm
import time


class SinglePromptModel:
    """Uses a single prompt with few-shot examples to classify our video into one of four labels.

    The model accepts a dataframe that contains video snippets.
    The model generates prompts using the snippets and queries
    the OpenAI API to classify the videos.

    Parameters
    ----------
    videos: pd.DataFrame
        The videos we want to create snippets for.
    save_path: str
        Where we want to save our predictions
    """

    def __init__(self, videos, save_path):
        self.videos = videos
        self.save_path = save_path


class BinaryPromptModel:
    """Cleans and condenses our YouTube videos into snippets that can be used to GPT classification.

    Accepts a dataframe containing YouTube
    video title, transcript, and tags and
    condenses it into a simple snippet that can be fed into GPT.
    Returns a dataframe with the snippets.

    Parameters
    ----------
    videos: pd.DataFrame
        The videos we want to create snippets for.
    save_path: str
        Where we want to save our data
    """

    def __init__(self):
        return


class FineTunedPromptModel:
    """Cleans and condenses our YouTube videos into snippets that can be used to GPT classification.

    Accepts a dataframe containing YouTube
    video title, transcript, and tags and
    condenses it into a simple snippet that can be fed into GPT.
    Returns a dataframe with the snippets.

    Parameters
    ----------
    videos: pd.DataFrame
        The videos we want to create snippets for.
    save_path: str
        Where we want to save our data
    """

    def __init__(self):
        return
