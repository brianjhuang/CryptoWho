#!/usr/bin/python
import os

class Classifier(object):
    """
    Static class that includes configuration for our model
    """

    # SAVE PATHS
    RESULTS_PATH = 'data/audit/youtube/results/'
    SEED_RESULTS_PATH = 'seed_predictions'
    CONFUSION_MATRIX_PATH = 'references/figures/seed_training_results.png'

    # LOAD PATHS
    SEED_LOAD_PATHS = ['data/seed/youtube/seed_videos.csv', 'data/seed/youtube/young_videos.csv', 'data/seed/youtube/old_videos.csv']