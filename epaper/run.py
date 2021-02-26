#!/usr/bin/env python3

import os, sys
import signal

from BitcoinPriceClient import BitcoinPriceClient
from PriceTicker import PriceTicker

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('exiting')
        self.kill_now = True

def run(strip):
    print('running')

if __name__ == '__main__':
    killer = GracefulKiller()
    price_client = BitcoinPriceClient('USD')    
    price_ticker = PriceTicker(price_client)

    try:
        while not killer.kill_now:
            price_ticker.run()

    except Exception as ex:
        print(ex)
        price_ticker.shutdown()
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

    price_ticker.shutdown()