#!/usr/bin/env python3

from decimal import Decimal

from TweetCreator import TweetCreator
from TweetValueExtractor import TweetValueExtractor
from TwitterBot import TwitterBot

from BitcoinClientMock import BitcoinClient
from TwitterClientMock import TwitterClient

TWEET = """\
#Bitcoin block 656900

Total supply: 18,542,940.19444435 BTC

Increase since yesterday:
+91 blocks
+568.75 BTC\
"""

def test_tweet_creator():
    creator = TweetCreator(
        656900,
        18542940.19444435,
        656809,
        18542371.44444435)

    actual = creator.create_tweet()
    expected = TWEET

    assert_equals(expected, actual)

def test_tweet_value_extractor():
    extractor = TweetValueExtractor(TWEET)

    actual = extractor.block_height()
    assert_equals(656900, actual)

    actual = extractor.total()
    assert_equals(Decimal('18542940.19444435'), actual)

def test_twitter_bot():
    bitcoin_client = BitcoinClient()
    twitter_client = TwitterClient()

    bot = TwitterBot(bitcoin_client, twitter_client)
    bot.run()
    
    actual = bot.tweet
    expected = TWEET

    assert_equals(expected, actual)

def assert_equals(expected, actual):
    if expected != actual:
        raise Exception('assertion failed', expected, actual)

def assert_true(condition):
    if not condition:
        raise Exception('assertion failed', condition)

def run_tests():
    test_tweet_creator()
    test_tweet_value_extractor()
    test_twitter_bot()

    print('complete')

if __name__ == '__main__':
    run_tests()