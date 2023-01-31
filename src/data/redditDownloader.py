import sys
# Provide access to main dir path for config, data, etc
sys.path.insert(0, '../../')

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
import sys
import pandas as pd
import re

# Config Imports
from config import reddit


from dataclasses import dataclass
@dataclass
class YoutubeLink:
    url: str
    subreddit: str
    thread_url: str
    
@dataclass
class TextEntry:
    text: str
    subreddit: str
    thread_url: str
    text_type: str
    
class Scraper():
    def __init__(self, scrape_depth = reddit.SCRAPE_DEPTH, subreddits = reddit.SUBREDDITS):
        self.SCRAPE_DEPTH = scrape_depth
        self.SUBREDDITS = subreddits
        self.YoutubeLinks = []
        self.TextEntries = []
    
        self.driver = webdriver.Firefox()
        
    def extract_subreddit(self, url):
        """Gets the subreddit from a URL

        Args:
            url (str): URL to extract subreddit from
        """
        subreddit = re.findall(r"/r/(\w+)/", url)[0]
        return subreddit
    
    def process_thread(self, url):
        """Scrapes a thread, saving the thread text, comment text, and any youtube links found

        Args:
            url (str): The url of the thread to scrape
        """
        
        # old.reddit.com is easier to scrape, doesn't have js lazy loading
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source)
        
        subreddit = self.extract_subreddit(url)
        
        main_thread = soup.find('div', {'class': 'expando'}).text
        self.TextEntries.append(TextEntry(main_thread, subreddit, url, 'thread'))
        
        #Find all links in comments, keeping only youtube links
        comments = soup.find_all('div', {"data-type": "comment"})
        for comment in comments:
            #Record comment text
            comment_text = comment.find('div', {'class': 'md'}).text
            self.TextEntries.append(TextEntry(comment_text, subreddit, url, 'comment'))
            
            #Record youtube links
            for link in comment.find('div', {'class': 'usertext-body'}).find_all('a', href=True):
                if 'youtube.com' in link['href']:
                    self.YoutubeLinks.append(YoutubeLink(link['href'], subreddit, url))
                    
    def process_subreddit(self, subreddit):
        """Gets thread links from a subreddit, up to a specified depth

        Args:
            subreddit (str): Name of subreddit to scrape

        Returns:
            list: List of all thread links found
        """
        url = f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t=year"
        self.driver.get(url)
        threads = []
        for i in range(self.SCRAPE_DEPTH):
            # Get all thread links
            soup = BeautifulSoup(self.driver.page_source)
            links = soup.find_all('a', {"class": "title"})
            threads += [link for link in links if link['href'].startswith('/r/')]
            
            self.driver.find_element(By.CLASS_NAME, 'next-button').click()

        return threads
    
    def scrape(self):
        """Scrapes all subreddits, saving all youtube links and text entries found
        """
        for subreddit in self.SUBREDDITS:
            threads = self.process_subreddit(subreddit)
            for thread in threads:
                thread_url = f"https://old.reddit.com{thread['href']}"
                self.process_thread(thread_url)
                
        self.driver.close()
                
    def save(self):
        pd.DataFrame(self.YoutubeLinks).to_csv(reddit.RAW_THREADS + 'scraped_youtube_links.csv', index=False)
        pd.DataFrame(self.TextEntries).to_csv(reddit.RAW_THREADS + 'scraped_comments.csv', index=False)
        
if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape()
    scraper.save()