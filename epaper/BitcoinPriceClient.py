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
    def __init__(self, currency):
        self.currency = currency

    def retrieve_price(self):
        data = self.retrieve_data()

        if not data:
            return 'N/A'

        price = data[self.currency]['last']
        symbol = data[self.currency]['symbol']
        return self.format_price(price, symbol)

    def format_price(self, price, symbol):
        price_without_cents = self.price_without_cents(price)
        return '{}{}'.format(symbol, price_without_cents)

    def price_without_cents(self, price):
        separator = '.'
        return str(price).split(separator, 1)[0]

    def retrieve_data(self):
        try:
            request = Request()
            result = request.get(SERVICE_ENDPOINT)
            if result:
                return json.loads(result)
        except ConnectionError as e:
            msg = str(e)
            logging.error(msg)
