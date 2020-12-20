import twitter

from utils.config import config

CONSUMER_KEY = config().get('twitter.api', 'consumer_key')
CONSUMER_SECRET = config().get('twitter.api', 'consumer_secret')
ACCESS_TOKEN_KEY = config().get('twitter.api', 'access_token_key')
ACCESS_TOKEN_SECRET = config().get('twitter.api', 'access_token_secret')

class TwitterClient(object):
    def api(self):
        return twitter.Api(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token_key=ACCESS_TOKEN_KEY,
            access_token_secret=ACCESS_TOKEN_SECRET)

    def get_latest_tweet(self):
        list = self.api().GetHomeTimeline(count=1, trim_user=True, exclude_replies=True, include_entities=False)
        return list[0].text

    def tweet(self, msg):
        self.api().PostUpdate(msg)
