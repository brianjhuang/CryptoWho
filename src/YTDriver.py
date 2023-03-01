### A modified version of the driver from the original paper, found here:
### https://github.com/ucdavis-noyce/YouTube-Driver
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from time import sleep
from src.utils import Video, VideoUnavailableException, time2seconds, AuditVideo
#from pyvirtualdisplay import Display
import os

class YTDriver:

    def __init__(self, browser='chrome', profile_dir=None, use_virtual_display=False, headless=False, verbose=False):
        """
        Initializes the webdriver and virtual display

        ### Arguments:
        - `browser`: Specify `chrome` or `firefox` to launch the corresponding webdriver.
        - `profile_dir`: Specify a directory to save the browser profile so it can be loaded later. Set to `None` to not save the profile.
        - `use_virtual_display`: Set to `True` to launch a virtual display using `pyvirtualdisplay`.
        - `headless`: Set to `True` to run the browser in headless mode.
        - `verbose`: Set to `True` to enable logging messages.
        """

        self.verbose = verbose

        # if use_virtual_display:
        #     self.__log("Starting virtual display")
        #     display = Display(size=(1920,1080))
        #     display.start()

        if browser == 'chrome':
            self.driver = self.__init_chrome(profile_dir, headless)
        elif browser == 'firefox':
            self.driver = self.__init_firefox(profile_dir, headless)
        else:
            raise Exception("Invalid browser", browser)

        self.driver.set_page_load_timeout(30)
        self.VIDEOS_WATCHED = 0

        self.video_recs = []
        self.homepage_recs = []

    def close(self):
        """
        Close the underlying webdriver.
        """
        self.driver.close()

    def get_homepage(self, scroll_times=0):
        """
        Collect videos from the YouTube homepage.

        ### Arguments:
        - `scroll_times`: Number of times to scroll the homepage.

        ### Returns:
        - List of videos of type `ytdriver.helpers.Video`.

        """
        # try to find the youtube icon
        try:
            self.__log('Clicking homepage icon')
            self.driver.find_element(By.ID, 'logo-icon').click()
        except:
            self.__log('Getting homepage via URL')
            self.driver.get('https://www.youtube.com')

        # wait for page to load
        sleep(2)

        # scroll page to load more results
        for _ in range(scroll_times):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            sleep(0.2)
            

        # collect video-like tags from homepage
        videos = self.driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-rich-item-renderer')

        # identify actual videos from tags
        homepage = []
        for video in videos:
            a = video.find_elements(By.TAG_NAME, 'a')[0]
            href = a.get_attribute('href')
            if href is not None and href.startswith('https://www.youtube.com/watch?'):
                homepage.append(Video(a, href))

        return homepage

    def get_recommendations(self, topn=5):

        """
        Collect up-next recommendations for the currently playing video.

        ### Arguments:
        - `topn`: Number of recommendations to return.

        ### Returns:
        - List of videos of type `ytdriver.helpers.Video`.
        
        """
        # wait for page to load
        sleep(2)

        # wait for recommendations
        elems = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'ytd-compact-video-renderer'))
        )

        # recommended videos array
        return [Video(elem, elem.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')) for elem in elems[:topn]]

    def search_videos(self, query, scroll_times=0):
        """
        Search for videos.

        ### Arguments:
        - `query` (`str`): Search query.

        ### Returns:
        - List of videos of type `ytdriver.helpers.Video`.
        
        """

        # load video search results
        self.driver.get('https://www.youtube.com/results?search_query=%s' % query)

        # wait for page to load
        sleep(2)

        # scroll page to load more results
        for _ in range(scroll_times):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            sleep(0.2)

        # collect video-like tags from homepage
        videos = self.driver.find_elements(By.XPATH, '//div[@id="contents"]/ytd-video-renderer')
        
        # identify actual videos from tags
        results = []
        for video in videos:
            a = video.find_elements(By.TAG_NAME, 'a')[0]
            href = a.get_attribute('href')
            if href is not None and href.startswith('https://www.youtube.com/watch?'):
                results.append(Video(a, href))
        return results


    def play(self, video, duration=5):
        """
        Play a video for a set duration. Returns when that duration passes.

        ### Arguments:
        - `video` (`str`|`ytdriver.helpers.Video`): Video object or URL to play.
        - `duration` (`int`): How long to play the video.
        
        """
        try:
            self.__click_video(video)
            self.__check_video_availability()
            self.__click_play_button()
            self.__handle_ads()
            #self.__clear_prompts()
            sleep(duration)
            self.VIDEOS_WATCHED += 1
        except Exception as e:
            self.__log(e)
            

    def play_list(self, videos, duration=5, homepage_interval=0):
        """
        Play a list of videos for a set duration. Returns when that duration passes.

        ### Arguments:
        - `videos` (`list`): List of video objects or URLs to play.
        - `duration` (`int`): How long to play each video.
        - `homepage_interval` (`int`): How often to scrape the homepage. (If 0, never scrape homepage.)
        
        """
        
        for i, video in enumerate(videos):
            self.play(video, duration)
            try:
                recs = self.get_recommendations()
                rec_urls = [rec.url for rec in recs]
                for rec_url in rec_urls:
                    audit_vid = AuditVideo(rec_url, video, self.VIDEOS_WATCHED)
                    self.video_recs.append(audit_vid)
            except Exception as e:
                self.__log("Failed to get recommendations.")
                self.__log(e)
            if homepage_interval and i % homepage_interval == 0:
                homepage_vids = self.get_homepage()
                for homepage_vid in homepage_vids:
                    audit_vid = AuditVideo(homepage_vid.url, 'homepage', self.VIDEOS_WATCHED)
                    self.homepage_recs.append(audit_vid)

    def save_screenshot(self, filename):
        """
        Save a screenshot of the current browser window.

        ### Arguments:
        - `filename`: Filename to save image as.
        """
        return self.driver.save_screenshot(filename)

    ## Helpers
    def __log(self, message):
        if self.verbose:
            print(message)

    def __click_video(self, video):
        if type(video) == Video:
            try:
                # try to click the element using selenium
                self.__log("Clicking element via Selenium...")
                video.elem.click()
                return
            except Exception as e:
                try:
                    # try to click the element using javascript
                    self.__log("Failed. Clicking via Javascript...")
                    self.driver.execute_script('arguments[0].click()', video.elem)
                except:
                    # js click failed, just open the video url
                    self.__log("Failed. Loading video URL...")
                    self.driver.get(video.url)
        elif type(video) == str:
            self.driver.get(video)
        else:
            raise ValueError('Unsupported video parameter!')

    def __check_video_availability(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/h1'))
            )
        except WebDriverException:
            raise VideoUnavailableException()

    def __click_play_button(self):
        try:
            playBtn = self.driver.find_elements(By.CLASS_NAME, 'ytp-play-button')
            if 'Play' in playBtn[0].get_attribute('title'):
                playBtn[0].click()
        except:
            pass

    def __handle_ads(self):
        # handle multiple ads
        while True:
            sleep(1)

            # check if ad is being shown
            preview = self.driver.find_elements(By.CLASS_NAME, 'ytp-ad-preview-container')
            if len(preview) == 0:
                self.__log('Ad not detected')
                # ad is not shown, return
                return

            self.__log('Ad detected')
            
            sleep(1)
            preview = preview[0]
            # an ad is being shown
            # grab preview text to determine ad type
            text = preview.text.replace('\n', ' ')
            wait = 0
            if 'after ad' in text:
                # unskippable ad, grab ad length
                length = self.driver.find_elements(By.CLASS_NAME, 'ytp-ad-duration-remaining')[0].text
                wait = time2seconds(length)
                self.__log('Unskippable ad. Waiting %d seconds...' % wait)
            elif 'begin in' in text or 'end in' in text:
                # short ad
                wait = int(text.split()[-1])
                self.__log('Short ad. Waiting for %d seconds...' % wait)
            else:
                # skippable ad, grab time before skippable
                wait = int(text)
                self.__log('Skippable ad. Skipping after %d seconds...' % wait)

            # wait for ad to finish
            sleep(wait)

            # click skip button if available
            skip = self.driver.find_elements(By.CLASS_NAME, 'ytp-ad-skip-button-container')
            if len(skip) > 0:
                skip[0].click()

    def __clear_prompts(self):
        try:
            sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/yt-tooltip-renderer/div[2]/div[1]/yt-button-renderer/a/tp-yt-paper-button/yt-formatted-string').click()
        except:
            pass
    
    def __init_chrome(self, profile_dir, headless):
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')

        if profile_dir is not None:
            options.add_argument('--user-data-dir=%s' % profile_dir)
        if headless:
            options.add_argument('--headless')

        return Chrome(options=options)

    def __init_firefox(self, profile_dir, headless):
        options = FirefoxOptions()
        options.add_argument('--window-size=1920,1080')
        if profile_dir is not None:
            pass
        if headless:
            options.add_argument('--headless')

        service = Service(log_path=os.path.devnull)
        return Firefox(options=options, service=service)


