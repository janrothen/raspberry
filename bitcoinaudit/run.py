#!/usr/bin/env python3

from BitcoinClient import BitcoinClient
from TwitterClient import TwitterClient

from TwitterBot import TwitterBot

def run():
	bitcoin_client = BitcoinClient()
	twitter_client = TwitterClient()

	bot = TwitterBot(bitcoin_client, twitter_client)
	bot.run()

if __name__ == '__main__':
	run()