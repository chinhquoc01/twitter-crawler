from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
'''Uncomment the below line when running in linux'''
# from pyvirtualdisplay import Display
import time, os
 
class Twitterbot:
 
    def __init__(self, email, password):
 
        """Constructor
 
        Arguments:
            email {string} -- registered twitter email
            password {string} -- password for the twitter account
        """
 
        self.email = email
        self.password = password
        # initializing chrome options
        chrome_options = Options()
 
        # adding the path to the chrome driver and 
        # integrating chrome_options with the bot
        self.bot = webdriver.Chrome()
 
    def login(self):
        """
            Method for signing in the user 
            with the provided email and password.
        """
 
        bot = self.bot
        # fetches the login page
        bot.get('https://x.com/login')
        # adjust the sleep time according to your internet speed
        time.sleep(3)
 
        email = bot.find_element(by=By.TAG_NAME,
            value='input'
        )

        # sends the email to the email input
        email.send_keys(self.email)

        email.send_keys(Keys.RETURN)

        time.sleep(2)

        password = bot.find_elements(by=By.TAG_NAME,
            value='input'
        )[1]
 
        # sends the password to the password input
        password.send_keys(self.password)
        # executes RETURN key action
        password.send_keys(Keys.RETURN)
 
        time.sleep(1)

    def convert_to_int(self, s):
        # Define a dictionary for suffix multipliers
        suffix_multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000}
        
        # Check if the string ends with a known suffix
        if s[-1] in suffix_multipliers:
            # Extract the numeric part and the suffix
            num_part = float(s[:-1])
            suffix = s[-1]
            
            # Multiply by the corresponding multiplier
            result = num_part * suffix_multipliers[suffix]
        else:
            # If no suffix, just convert the string to a float
            result = float(s)
        
        # Convert the result to an integer
        return int(result)
 
    def crawl_data(self, hashtag):
 
        """
        This function automatically retrieves
        the tweets and then likes and retweets them
 
        Arguments:
            hashtag {string} -- twitter hashtag
        """
 
        bot = self.bot
 
        # fetches the latest tweets with the provided hashtag
        bot.get(
            f'https://x.com/search?q={hashtag}&src=typed_query'
        )
 
        time.sleep(3)

        tweets = bot.find_elements(by=By.TAG_NAME, value='article')

        data = list()

        for tweet in tweets:
            a_tags = tweet.find_elements(by=By.TAG_NAME, value='a')
            hashtag_tags = []
            for a_tag in a_tags:
                if 'hashtag' in a_tag.get_attribute('href'):
                    hashtag_tags.append(a_tag.text)

            button_tags = tweet.find_elements(by=By.TAG_NAME, value='button')

            author = a_tags[2].text

            submit_time = tweet.find_element(by=By.TAG_NAME, value='time').get_attribute('datetime')
            content = tweet.find_element(by=By.XPATH, value='div/div/div[2]/div[2]/div[2]').text
            count_view = self.convert_to_int(a_tags[len(a_tags) - 1].find_element(by=By.XPATH, value='div/div[2]/span/span/span').text)
            article_link = a_tags[len(a_tags) - 1].get_attribute('href').replace('/analytics', '')
            count_like = self.convert_to_int(button_tags[3].find_element(by=By.XPATH, value='div/div[2]').text)

            tweet_data = {
                "author": author,
                "submit_time": submit_time,
                "content": content,
                "count_view": count_view,
                "count_like": count_like,
                "article_link": article_link,
                "hashtags": hashtag_tags
                }
            data.append(tweet_data)

        return data