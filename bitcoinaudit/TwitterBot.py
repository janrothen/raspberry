from TweetValueExtractor import TweetValueExtractor
from TweetCreator import TweetCreator

class TwitterBot(object):

    def __init__(self, bitcoin_client, twitter_client):
        self.bitcoin_client = bitcoin_client
        self.twitter_client = twitter_client

    def run(self):
        self.retrieve_stats()
        self.tweet_stats()

    def retrieve_stats(self):
        self.retrieve_current_stats()
        self.retrieve_yesterdays_stats()

    def tweet_stats(self):
        self.tweet = self.create_tweet()
        self.twitter_client.tweet(self.tweet)

    def retrieve_current_stats(self):
        self.current_block_height = self.bitcoin_client.get_block_height()
        self.current_total = self.bitcoin_client.get_total_amount()

    def retrieve_yesterdays_stats(self):
        yesterdays_tweet = self.twitter_client.get_latest_tweet()
        tweet_value_extractor = TweetValueExtractor(yesterdays_tweet)
        self.yesterdays_block_height = tweet_value_extractor.block_height()
        self.yesterdays_total = tweet_value_extractor.total()

    def create_tweet(self):
        tweet_creator = TweetCreator(
            self.current_block_height,
            self.current_total,
            self.yesterdays_block_height,
            self.yesterdays_total)
        return tweet_creator.create_tweet()