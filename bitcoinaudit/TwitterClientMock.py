MOCK_DATA = 'mock_data_twitter_latest_tweet.txt'

class TwitterClient(object):
    def get_latest_tweet(self):
        with open(MOCK_DATA, 'rb') as file_object:
            return file_object.read().decode('utf-8')

    def tweet(self, msg):
        print(msg)
