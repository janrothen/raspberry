#!/usr/bin/env python3

from BitcoinClient import BitcoinClient
#from BitcoinClientMock import BitcoinClient
from TwitterClient import TwitterClient
#from TwitterClientMock import TwitterClient

from TwitterBot import TwitterBot

bitcoin_client = BitcoinClient()
twitter_client = TwitterClient()

bot = TwitterBot(bitcoin_client, twitter_client)
bot.run()