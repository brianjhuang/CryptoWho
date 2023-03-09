import pandas as pd
import numpy as np

import os
import sys
import logging
from tqdm import tqdm
import time

import openai
from sklearn.metrics import accuracy_score, classification_report
from config import classifier

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


class ChatCompletionModel:

    def __init__(self, data, save_path):
        self.data = data
        self.save_path = save_path
        self.results = pd.DataFrame()

    def set_data(self, data):
        """Set the data"""
        self.data = data

    def set_save_path(self, save_path):
        """Set the save path"""
        self.save_path = save_path

    def get_data(self):
        """Get the data"""
        return self.data
    
    def get_save_path(self):
        """Get the save path"""
        return self.save_path
    
    def get_results(self):
        """Get the results"""
        return self.results
    
    def get_cost(self):
        """Get the cost if available"""
        # TURBO COST
        TURBO_COST = 0.00200 / 1000
        if len(self.results) <= 0:
            return 0
        else:
            return sum(self.results['total_tokens'] * TURBO_COST) 

    def create_messages(self, snippet):
        '''
        Create the messages that are sent in a single API call to the Chat Completions API endpoint.
        Sets the system message, prompts with instructions and affirms them with the first assistant message, and 
        prompts for the video snippet.

        Parameters
        ----------
        snippet : str
            The YouTube video snippet, consisting of the video title, summarized transcript, and tags.
        
        Returns
        -------
        list
            A list of the messages. Messages are stored as dictionaries with {role: "", content: ""}
        '''
        messages = [
            {"role": "system", "content" : "You are a classifier that determines if a YouTube video snippet falls under a label. A snippet is a concatenation of the video title, summarized transcript, and video tags. The labels and additional instructions will be included in the first user message."},
            {"role": "user", "content" : """Labels:

    Traditional: Videos that recommend or educate about stocks, bonds, real estate, commodities, retirement accounts, or other traditional investments or keywords related to them.
    Blockchain: Videos that recommend or educate about cryptocurrency (BTC, ETH, etc.), NFTs, or other Web3 investments or keywords related to them.
    Mixed: Videos that recommend or educate about both blockchain and traditional investments or keywords related to both.
    Unrelated: Videos that do not recommend or educate about either blockchain or traditional investments or keywords related to them.

    Instructions:
    - The classifier should consider the context and meaning of the keywords used to determine whether the snippet is related to traditional or blockchain investments.
    - If talks about making money from jobs, side hustles, or other alternative assets (cars, watches, artificial intelligence, trading cards, art, etc), they are Unrelated.
    - A video that is only downplaying an investment or discussing it negatively should be classified as Unrelated.
    - Please return predictions in the format" {Label} : {20 word or shorter rationale}"""},
            {"role": "assistant", "content": """Understood. I will classify YouTube video snippets based on the provided labels and instructions. Here's how I will format the predictions:

    {Label} : {20-word or shorter rationale}

    Please provide me with the YouTube video snippet you would like me to classify."""},
        ]
        
        snippet_message = {"role" : "user", "content" : snippet.replace("\n", " ").replace("  ", " ")}
        
        messages.append(snippet_message)
        
        return messages
    
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def classify_message(self, messages, temp = 0.25):
        '''
        Given a set of messages, query the OpenAI endpoint to retrieve our prediction.

        Parameters
        ----------
        messages : list
            A list of the messages. Messages are stored as dictionaries with {role: "", content: ""}
        temp : float
            The temperature of the model. Default 0.25        
        Returns
        -------
        openai.ChatCompletion.object
            Our prediction, formatted as a chat completion object.
        '''
        chatCompletion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temp
        )
        return chatCompletion
    
    def classify(self):
        '''
        Classify the entire dataset.

        Returns
        -------
        pd.DataFrame
            All of our predictions
        '''

        print("Created messages.")
        logging.info("Created messages.")
        self.data['messages'] = self.data['snippet'].apply(lambda x: self.create_messages(x))

        pbar = tqdm(self.data.iterrows())
        completions = []
        df = pd.DataFrame()
        saved_files = os.listdir(classifier.RESULTS_PATH)

        if f'progress_{self.save_path}.csv' in saved_files:
        
            print('Progress found, starting from where we left off.')
            logging.info('Progress found, starting from where we left off.')
            df = pd.read_csv(classifier.RESULTS_PATH + f'progress_{self.save_path}.csv')

        for idx, entry in pbar:
            # If we have progress and the video ID of our entry is in the progress
            if len(df) > 0 and entry['video_id'] in list(df['video_id']):
                print("Video already classified, moving on...")
                logging.info("Video already classified, moving on...")
                pbar.set_description("Video already classified, moving on...")
                continue
            else:
                pbar.set_description("Processing %s" % entry['title'])

            try:
                body = self.classify_message(entry['messages'])
                
                completion = dict(body['choices'][0]['message'])
                try:
                    prediction = completion['content'].split(':')[0].strip()
                    reason = completion['content'].split(':')[1].strip()
                except:
                    prediction = "Unrelated"
                    reason = completion['content']

                # ## Deal with Label: prefix that sometimes occurs
                # if 'label' in prediction.lower():
                #     prediction = prediction.lower().strip('label').strip('label:').strip().strip(":").strip().split(" ")[0]
                #     prediction = prediction[0].upper() + prediction[1:]

                completion['prediction']  = prediction
                completion['reason'] = reason
                completion['message'] = entry['messages']

                ## Save information from entry
                completion['video_id'] = entry['video_id']
                completion['title'] = entry['title']
                completion['transcript'] = entry['cleaned_transcript']
                completion['snippet'] = entry['snippet']
                completion['link'] = entry['link']
                
                ## Grab meta data
                completion.update({key: body[key] for key in ['created', 'id', 'model', 'object']})
                
                ## Grab token usage
                completion.update(dict(body['usage']))

                completions.append(completion)
                time.sleep(5)

            except Exception as e:
                # If we run into any error
                print(f"Ran into exception, saving progress and stopping.")
                logging.info(f"Ran into exception saving progress and stopping.")

                print(f"Exception: {e}")
                logging.info(f"Exception: {e}")

                df = pd.concat([df, pd.DataFrame(completions)])

                self.results = df
                df.to_csv(classifier.RESULTS_PATH + f'progress_{self.save_path}.csv', index_label = False)

                print("Saved file to:  {0}".format(classifier.RESULTS_PATH  + f'progress_{self.save_path}.csv'))
                logging.info("Saved file to:  {0}".format(classifier.RESULTS_PATH + f'progress_{self.save_path}.csv'))        

                return df    

        df = pd.concat([df, pd.DataFrame(completions)])

        df.to_csv(classifier.RESULTS_PATH + self.save_path + ".csv", index = False)

        print("Saved file to:  {0}".format(classifier.RESULTS_PATH + self.save_path + ".csv"))
        logging.info("Saved file to:  {0}".format(classifier.RESULTS_PATH + self.save_path + ".csv"))

        self.results = df

        return df
