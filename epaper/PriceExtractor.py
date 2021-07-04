class PriceExtractor(object):
    def __init__(self, currency, symbol):
        self.currency = currency
        self.symbol = symbol

    def formatted_price_from_data(self, data):
        if not data:
            return 'N/A'

        price = data[self.currency]['last']
        return self.format_price(price, self.symbol)

    def format_price(self, price, symbol):
        price_without_cents = self.price_without_cents(price)
        price_in_k = price_without_cents / 1000
        return '{}{:.1f}k'.format(symbol, price_in_k)

    def price_without_cents(self, price):
        separator = '.'
        price_without_cents = str(price).split(separator, 1)[0]
        return float(price_without_cents)