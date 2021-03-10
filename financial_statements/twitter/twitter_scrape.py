# ==================================================================
# This is for querying tweet objects that are scraped using snscrape
# ==================================================================

import pandas as pd
import tweepy
import csv
import snscrape.modules.twitter as sntwitter



consumer_key = "aaaaaaaaaaaaaaaaaaaaa" 
consumer_secret = "aaaaaaaaaaaaaaaaaaaaaaaa" 
access_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" 
access_token_secret = "aaaaaaaaaaaaaaaaaaaaaaaaaa"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet_url = pd.read_csv("Your_Text_File.txt", index_col= None,
header = None, names = ["links"])

af = lambda x: x["links"].split("/")[-1]
tweet_url['id'] = tweet_url.apply(af, axis=1)
tweet_url.head()

ids = tweet_url['id'].tolist()
total_count = len(ids)
chunks = (total_count - 1) // 50 + 1

def fetch_tw(ids):
    """
    Collect Tweet objects from csv or text file.
    """
    list_of_tw_status = api.statuses_lookup(ids, tweet_mode= "extended")
    empty_data = pd.DataFrame()
    for status in list_of_tw_status:
            tweet_elem = {"date": status.created_at,
                     "tweet_id":status.id,
                     "tweet":status.full_text,
                     "User location":status.user.location,
                     "Retweet count":status.retweet_count,
                     "Like count":status.favorite_count,
                     "Source":status.source}
            empty_data = empty_data.append(tweet_elem, ignore_index = True)
    empty_data.to_csv("new_tweets.csv", mode="a")

for i in range(chunks):
        batch = ids[i*50:(i+1)*50]
        result = fetch_tw(batch)


# =================================
# Scrape Twitter Data with snscrape
# =================================


class TweetScraper:

    def __init__(self, max_tweets=0):
        """
        Constructor
        """
        self.max_tweets = max_tweets
        self.tweets_list = []

    def scrape_username(self, name=String):
        """
        Scrapes Twitter data based off username (specific users)
        """
        for i, tweet in enumerate(sntwitter.TwitterSearchScrapper('from:{name}').get_items()):
            if i > self.max_tweets:
                break
            self.tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

        tweets_df = pd.DataFrame(self.tweets_list, columns=['datetime', 'id', 'text', 'username'])

        tweets_df.to_csv('tweets_username.csv', sep=',', index=False)

    def scrape_text_search(self, text=String):
        """
        Scrapes Twitter using textual query
        """
        for i, tweet in enumerate(sntwitter.TwitterSearchScrapper(text).get_items()):
            if i > self.max_tweets:
                break
            self.tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

        tweets_df = pd.DataFrame(self.tweets_list, columns=['datetime', 'id', 'text', 'username'])

        tweets_df.to_csv('tweets_text_query.csv', sep=',', index=False)
        
