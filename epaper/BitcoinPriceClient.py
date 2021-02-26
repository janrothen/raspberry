#!/usr/bin/env python3

# Checks if bitcoin node is reachable from outside
# Sends a notification email otherwise

import sys, traceback

import json

from utils.Request import Request
from utils.config import config

SERVICE_ENDPOINT = config().get('bitcoin.price', 'service_endpoint')

class BitcoinPriceClient(object):
	def __init__(self):
		self.price = None

	def retrieve_price(self, currency):
		try:
			request = Request()
			data = self.retrieve_data(request)
			print(data)
			price = data[currency]['last']
			symbol = data[currency]['symbol']
			self.price = '{}{}'.format(symbol, price)
		except ConnectionError as e:
			msg = str(e)
			self.price = 'N/A'

		return self.price

	def retrieve_data(self, request):
		data = {}
		result = request.get(SERVICE_ENDPOINT)
		if result:
			data = json.loads(result)
		return data
