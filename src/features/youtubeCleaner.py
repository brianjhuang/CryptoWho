import pandas as pd
import numpy as np
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.summarization import summarize

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
    '''

    def __init__(self, videos):
        self.videos = videos

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

        # Fill in remaining values with empty string. We can work without tags
        return df.fillna("")
    
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

        # If we have less than N words, we don't need to summarize
        if len(corpus) < n:
            return corpus
        # If we have less than a sentence, we also don't need TF-IDF
        elif len(corpus.split(".")) <= 1:
            return corpus

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
    
    def condense(self, corpus, word_count = 250):
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

        corpus = corpus.replace("\n", " ").replace(" - ", "").replace('- ', "").replace("\'", "").replace(".", ". ")
        
        # If we have less than 250 words, we don't need to summarize
        if len(corpus) < word_count:
            return corpus
        # If we have less than a sentence, we also don't summarize
        elif len(corpus.split(".")) <= 1:
            return corpus
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
    
    def createVideoSnippet(self, title = "", description = "", transcript = "", tags = ""):
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
        return
    
