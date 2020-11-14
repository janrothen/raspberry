from TweetValueExtractor import TweetValueExtractor
from TweetCreator import TweetCreator

class TwitterBot(object):

	def __init__(self, bitcoin_client, twitter_client):
		self.bitcoin_client = bitcoin_client
		self.twitter_client = twitter_client

	def run(self):
		# retrieve current stats from bitcoin full node
		current_block_height = self.bitcoin_client.get_block_height()
		current_total = self.bitcoin_client.get_total_amount()

		# extract yesterdays stats from yesterdays tweet
		yesterdays_tweet = self.twitter_client.get_latest_tweet()
		tweet_value_extractor = TweetValueExtractor(yesterdays_tweet)
		yesterdays_block_height = tweet_value_extractor.block_height()
		yesterdays_total = tweet_value_extractor.total()

		# create todays tweet
		tweet_creator = TweetCreator(
			current_block_height,
			current_total,
			yesterdays_block_height,
			yesterdays_total)
		tweet = tweet_creator.create_tweet()

		# tweet it
		self.twitter_client.tweet(tweet)
