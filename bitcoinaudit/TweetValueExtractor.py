import re
from decimal import Decimal

class TweetValueExtractor(object):
    def __init__(self, tweet):
        self.tweet = tweet

    def block_height(self):
        block_height = self.extract_snippet_between('block', 'Total')
        return int(block_height)

    def total(self):
        total = self.extract_snippet_between('supply', 'BTC')
        total = total.replace(',', '')
        return Decimal(total)

    def extract_snippet_between(self, start, end):
        s = re.search(start, self.tweet)
        s_index_end = s.end() + 1

        e = re.search(end, self.tweet)
        e_index_start = e.start() - 1
        result = self.tweet[s_index_end:e_index_start]
        return result.strip(' \t\n\r')