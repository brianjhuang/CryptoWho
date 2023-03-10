import pandas as pd
import numpy as np
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization import summarize

from config import youtube

class Cleaner():
    ''' Cleans and condenses our YouTube videos into snippets that can be used to GPT classification.

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
    '''

    def __init__(self, videos, save_path = youtube.SEED_VIDEOS + 'processed_seed_videos.csv', use_ratio = False, ratio = 0.2, max_word_count = 250):
        self.videos = videos
        self.save_path = save_path
        self.max_word_count = max_word_count
        self.use_ratio = use_ratio
        self.ratio = ratio

    def getVideos(self):
        """
        Gets all of our videos.

        Returns
        -------
        pd.DataFrame
            Our videos
        """

        return self.videos
    
    def setVideos(self, videos):
        """
        Sets our new videos.

        Parameters
        ----------
        videos : pd.DataFrame
            Our new videos
        """

        self.videos = videos

    def getSavePath(self):
        """
        Gets all of our save_path.

        Returns
        -------
        pd.DataFrame
            Our save_path
        """

        return self.save_path
    
    def setSavePath(self, save_path):
        """
        Sets our new save_path.

        Parameters
        ----------
        videos : pd.DataFrame
            Our new save_path
        """

        self.save_path = save_path

    def getMaxWordCount(self):
        """
        Gets all of our max_word_count.

        Returns
        -------
        pd.DataFrame
            Our max_word_count
        """

        return self.max_word_count
    
    def setMaxWordCount(self, max_word_count):
        """
        Sets our new max_word_count.

        Parameters
        ----------
        videos : pd.DataFrame
            Our new max_word_count
        """

        self.max_word_count = max_word_count

    def getUseRatio(self):
        """
        Gets all of our use_ratio.

        Returns
        -------
        pd.DataFrame
            Our use_ratio
        """

        return self.use_ratio
    
    def setUseRatio(self, use_ratio):
        """
        Sets our new use_ratio.

        Parameters
        ----------
        videos : pd.DataFrame
            Our new use_ratio
        """

        self.use_ratio = use_ratio

    def getRatio(self):
        """
        Gets all of our ratio.

        Returns
        -------
        pd.DataFrame
            Our ratio
        """

        return self.ratio
    
    def setRatio(self, ratio):
        """
        Sets our new ratio.

        Parameters
        ----------
        videos : pd.DataFrame
            Our new ratio
        """

        self.ratio = ratio

    def remove_nulls(self):
        """
        Removes all the null values from our dataframe.

        Returns
        -------
        pd.DataFrame
            Our cleaned dataframe
        """
        # Remove videos with no transcript
        df = self.videos.dropna(subset = ['cleaned_transcript', 'title']).reset_index(drop = True)
        
        self.videos = df.fillna("")

        # Fill in remaining values with empty string. We can work without tags
        return self.videos
    
    def clean_text(self, corpus):
        """Applies TF-IDF on a text corpus to extract the N most important words/phrases

        Parameters
        ----------
        corpus : str
            The body of text we want to clean
        
        Returns
        -------
        corpus
            The cleaned text
        """

        # Removes leading and trailing periods, newlines, dashes, and spaces.
        return corpus.strip('.\n- ')
    
    def applyTfidf(self, corpus, n):
        """ Applies TF-IDF on a text corpus to extract the N most important words/phrases

        Parameters
        ----------
        corpus : str
            The body of text we want to extract words from.
        n : int
            The number of words we want. Default 10
        
        Returns
        -------
        list
            The top N words.
        """
        # Convert the text into a sparse matrix using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([corpus])
        
        # Get the feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = dict(zip(feature_names, tfidf.data))
        
        # Sort the scores in descending order
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Select only the top N features
        selected_features = [x[0] for x in sorted_scores[:n]]
        
        return selected_features

    def condenseTfidf(self, corpus, n):
        """ Applies TF-IDF on a text corpus to extract the N most important words/phrases

        Parameters
        ----------
        corpus : str
            The body of text we want to extract words from.
        n : int
            The number of words we want. Default 10
        
        Returns
        -------
        list
            The top N words.
        """
        
        # If we have less than N words, we don't need to summarize
        if len(corpus.split(" ")) < n:
            return corpus
        # If we have less than a sentence, we also don't need TF-IDF
        if len(corpus.split(". ")) <= 1:
            corpus += '.'

        corpus = corpus.replace("\n", " ").replace(" - ", "").replace('- ', "").replace("\'", "").replace(".", ". ")
        corpus = corpus.replace("U.S.", "United States").replace("U.S", "United States").replace("U.S.A", "United States").replace("U.S.A.", "United States")

        # Convert the text into a sparse matrix using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([corpus])
        
        # Get the feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = dict(zip(feature_names, tfidf.data))
        
        # Sort the scores in descending order
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Select only the top N features
        selected_features = [x[0] for x in sorted_scores[:n]]
        
        return selected_features
    
    def condense(self, corpus, word_count = 250, ratio = 0.2):
        """Applies gensim summarization using TextRank to summarize a corpus of text.

        Parameters
        ----------
        corpus : str
            The body of text we want to extract words from.
        word_count : int
            The number of words we want in our summary. Default 250
        
        Returns
        -------
        str
            The top tags seperate by spaces
        """
        
        word_count = self.max_word_count
        ratio = self.ratio
        
        # If we have less than 250 characters, we don't need to summarize
        if len(corpus.split(" ")) < word_count:
            return corpus
        # If we have less than a sentence, make it a sentence
        if len(corpus.split(". ")) <= 1:
            corpus += '.'
        
        corpus = corpus.replace("U.S.", "United States").replace("U.S", "United States").replace("U.S.A", "United States").replace("U.S.A.", "United States")
        corpus = corpus.replace("\n", " ").replace(" - ", "").replace('- ', "").replace("\'", "").replace(".", ". ")
        
        if self.use_ratio:
            return summarize(corpus, ratio = ratio)
        
        return summarize(corpus, word_count = word_count)
    
    def topTags(self, tags, n = 10):
        """ Applies TF-IDF on YouTube tags to get the most relevant tags. Cleans the text.

        Parameters
        ----------
        corpus : str
            The body of text we want to extract words from.
        n : int
            THe number of tags we want. Default 10
        
        Returns
        -------
        str
            The top tags seperate by spaces
        """
        corpus = " ".join([tag.strip().strip("\'") for tag in tags[1:-1].strip('[').strip(']').split(',')])
        
        if len(corpus) == 0:
            return ""
        
        selected_features = self.applyTfidf(corpus, n)
        
        return " ".join(selected_features)
    
    def createVideoSnippet(self, title = "", description = "", transcript = "", tags = "", tfidf = False, use_desc = False):
        """ Creates the video snippet.
        
        Parameters
        ----------
        title : str
            The title of our video
        description: str
            The cleaned description of our video.
        transcript: str
            The cleaned transcript of our video
        tags: str
            The TF-IDF of our tags
        
        Returns
        -------
        pd.DataFrame
            The top tags seperate by spaces
        """

        title = self.clean_text(title)
        
        if tfidf:
            if use_desc:
                description = self.clean_text(self.condenseTfidf(description, 100))
            transcript = self.clean_text(self.condenseTfidf(transcript, 200))
        else:
            if use_desc:
                description = self.clean_text(self.condense(description, 100))
            transcript = self.clean_text(self.condense(transcript))

        tags = self.clean_text(self.topTags(tags))
        
        if use_desc:
            return title + ". " + description + ". " + transcript + ". " + tags + "."

        return title + ". " + transcript + ". " + tags + "." 
    
    def generateVideoSnippets(self, tfidf = False, use_desc = False):
        """ Creates the video snippets for all videos.
        
        Returns
        -------
        pd.DataFrame
            The videos with snippets appended.
        """
        
        self.remove_nulls()

        self.videos['snippet'] = self.videos.apply(lambda x: self.createVideoSnippet(x.title, x.description, x.cleaned_transcript, x.tags, tfidf, use_desc), axis = 1)
        
        self.videos.to_csv(self.save_path)
        return self.videos