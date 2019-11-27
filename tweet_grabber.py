import tweepy
import numpy as np
import config as cfg

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.result = {}

    def on_status(self, tweet):
        self.result['tweet_created_at'] = tweet.created_at
        self.result['id_str'] = tweet.id_str
        self.result['text'] = tweet.text
        self.result['source'] = tweet.source
        self.result['user_id'] = tweet.user.id_str
        self.result['screen_name'] = tweet.user.screen_name
        self.result['location'] = tweet.user.location
        self.result['url'] = tweet.user.url
        self.result['user_name'] = tweet.user.name
        self.result['followers_count'] = tweet.user.followers_count
        self.result['friends_count'] = tweet.user.friends_count
        self.result['user_created_at'] = tweet.user.created_at
        self.result['language'] = tweet.lang
        return False

    def on_error(self, status):
        print("Error detected")

# Twitter Authentication
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

# Function to execute the stream and return the tweet
def run_api(filter):
    tweets_listener = StreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=[filter], languages=["en"])
    return tweets_listener.result

