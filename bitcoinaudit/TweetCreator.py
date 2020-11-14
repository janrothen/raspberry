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

	def create_tweet(self):
		total_formatted = f"{self.total_current:,}"
		increase_blocks_formatted = f"{self.block_height_increase_since_yesterday():,}"
		increase_total_formatted = f"{self.total_increase_since_yesterday():,}"
		increase_total_formatted = increase_total_formatted.rstrip('0').rstrip('.')

		return self.msg_template().format(
			height=self.height_current,
			total=total_formatted,
			increase_blocks=increase_blocks_formatted,
			increase_total=increase_total_formatted)

	def msg_template(self):
		return """#Bitcoin block {height}

Total supply: {total} BTC

Increase since yesterday:
+{increase_blocks} blocks
+{increase_total} BTC"""