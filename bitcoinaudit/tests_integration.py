#!/usr/bin/env python3

from BitcoinClient import BitcoinClient
from TwitterClient import TwitterClient

TWEET = """\
#Bitcoin block 656900

Total supply: 18,542,940.19444435 BTC

Increase since yesterday:
+91 blocks
+568.75 BTC\
"""

def test_bitcoin_client():
    client = BitcoinClient()
    
    connection_count = client.get_connection_count()

    assert_true(connection_count >= 0)

def test_twitter_client():
    client = TwitterClient()
    
    latest_tweet = client.get_latest_tweet()

    assert_not_none(latest_tweet)
    assert_true('#Bitcoin' in latest_tweet)

def assert_true(condition):
    if not condition:
        raise Exception('assertion failed', condition)

def assert_not_none(condition):
    if condition is None:
        raise Exception('assertion failed', condition)

def run_tests():
    test_bitcoin_client()
    test_twitter_client()

    print('complete')

if __name__ == '__main__':
    run_tests()