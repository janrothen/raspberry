#!/usr/bin/env python3

from decimal import Decimal

from TweetCreator import TweetCreator
from TweetValueExtractor import TweetValueExtractor
from TwitterBot import TwitterBot

from BitcoinClientMock import BitcoinClient
from TwitterClientMock import TwitterClient

TWEET = """\
#Bitcoin block 657413

Total supply: 18,546,158.94441705 BTC

Increase since yesterday:
+151 blocks
+956.2499727 BTC\
"""

def test_tweet_creator():
    creator = TweetCreator(
        657413,
        Decimal('18546158.94441705'),
        657262,
        Decimal('18545202.69444435'))

    actual = creator.create_tweet()
    expected = TWEET

    assert_equals(expected, actual)

def test_tweet_creator_formatting():
    creator = TweetCreator(0, Decimal('0'), 0, Decimal('0'))
    actual = creator.total_increase_since_yesterday_formatted()
    assert_equals('0', actual)
    creator = TweetCreator(0, Decimal('10'), 0, Decimal('9'))
    actual = creator.total_increase_since_yesterday_formatted()
    assert_equals('1', actual)
    creator = TweetCreator(0, Decimal('10.5'), 0, Decimal('9.49999999'))
    actual = creator.total_increase_since_yesterday_formatted()
    assert_equals('1.00000001', actual)
    creator = TweetCreator(0, Decimal('10.50000000'), 0, Decimal('9.40000000'))
    actual = creator.total_increase_since_yesterday_formatted()
    assert_equals('1.1', actual)
    creator = TweetCreator(0, Decimal('18546158.94441705'), 0, Decimal('18545202.69444435'))
    actual = creator.total_increase_since_yesterday_formatted()
    assert_equals('956.2499727', actual)

def test_tweet_value_extractor():
    extractor = TweetValueExtractor(TWEET)

    actual = extractor.block_height()
    assert_equals(657413, actual)

    actual = extractor.total()
    assert_equals(Decimal('18546158.94441705'), actual)

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
    test_tweet_creator_formatting()
    test_tweet_value_extractor()
    test_twitter_bot()

    print('complete')

if __name__ == '__main__':
    run_tests()