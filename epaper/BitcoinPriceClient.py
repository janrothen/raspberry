#!/usr/bin/env python3

# Checks if bitcoin node is reachable from outside
# Sends a notification email otherwise

import sys, traceback
import logging

import json

from utils.Request import Request
from utils.config import config

SERVICE_ENDPOINT = config().get('bitcoin.price', 'service_endpoint')

class BitcoinPriceClient(object):
	def retrieve_price(self, currency):
		data = self.retrieve_data()
		logging.debug(data)

		if not data:
			return 'N/A'

		price = data[currency]['last']
		symbol = data[currency]['symbol']
		price_formatted = '{}{}'.format(symbol, price)
		logging.info(price_formatted)

		return price_formatted

	def retrieve_data(self):
		try:
			request = Request()
			result = request.get(SERVICE_ENDPOINT)
			if result:
				return json.loads(result)
		except ConnectionError as e:
			msg = str(e)
			logging.error(msg)
