#!/usr/bin/env python3

from BitcoinPriceClient import BitcoinPriceClient
from PriceTicker import PriceTicker

def run():
    price_client = BitcoinPriceClient('USD')    

    price_ticker = PriceTicker(price_client)
    price_ticker.run()

if __name__ == '__main__':
    run()
