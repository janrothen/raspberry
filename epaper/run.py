#!/usr/bin/env python3

import os, sys
import signal
import logging

from BitcoinPriceClient import BitcoinPriceClient
from PriceTicker import PriceTicker

logging.basicConfig(level=logging.DEBUG)

class GracefulKiller:
    kill_now = False

    def __init__(self, ticker):
        self.ticker = ticker

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('exiting...')
        self.ticker.shutdown()

if __name__ == '__main__':
    price_client = BitcoinPriceClient('USD')    
    price_ticker = PriceTicker(price_client)

    killer = GracefulKiller(price_ticker)

    try:
        price_ticker.run()
    except Exception as ex:
        logging.error(ex)
        
        price_ticker.shutdown()

        traceback.print_exc(file=sys.stdout)
        sys.exit(0)