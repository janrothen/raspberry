import re
from decimal import Decimal

class TweetCreator(object):
    def __init__(self, height_current, total_current, height_yesterday, total_yesterday):
        self.height_current = height_current
        self.height_yesterday = height_yesterday
        self.total_current = total_current
        self.total_yesterday = total_yesterday

    def block_height_increase_since_yesterday(self):
        return self.height_current - self.height_yesterday

    def total_increase_since_yesterday(self):
        return self.total_current - self.total_yesterday

    def total_increase_since_yesterday_formatted(self):
        total = self.total_increase_since_yesterday()
        if total == 0:
            return '0'

        formatted = f'{total:,}'
        return formatted.rstrip('0').rstrip('.')

    def create_tweet(self):
        return self.msg_template().format(
            height=self.height_current,
            total=f'{self.total_current:,}',
            increase_blocks=f'{self.block_height_increase_since_yesterday():,}',
            increase_total=self.total_increase_since_yesterday_formatted()
        )

    def msg_template(self):
        return """\
#Bitcoin block {height}

Increase since yesterday:
+{increase_blocks} blocks
+{increase_total} BTC

Total supply: {total} BTC\
"""