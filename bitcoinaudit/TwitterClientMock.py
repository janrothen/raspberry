MOCK_DATA = 'mock_data_twitter_latest_tweet.txt'

class TwitterClient(object):
	def get_latest_tweet(self):
		file_object = open(MOCK_DATA, 'r')
		return file_object.read()

	def tweet(self, msg):
		print(msg)
