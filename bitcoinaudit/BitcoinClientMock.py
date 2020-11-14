from decimal import Decimal

class BitcoinClient(object):
	@property
	def getconnectioncount(self):
		return 39

	@property
	def gettxoutsetinfo(self):
		return {
			'height': 656900,
			'bestblock': '0000000000000000000ade5918aa3b331ffc6e642b9b69a12852471545962005',
			'transactions': 42139294,
			'txouts': 68283152,
			'bogosize': 5126540942,
			'hash_serialized_2':
			'b3aa44784be7853afbe6aa223a1d1555176b44158e392a1d221c4645ee366907',
			'disk_size': 4201046441,
			'total_amount': Decimal('18542940.19444435')
		}
	
	def get_block_height(self):
		return BitcoinClient().gettxoutsetinfo['height']
	
	def get_total_amount(self):
		return BitcoinClient().gettxoutsetinfo['total_amount']

	def get_connection_count(self):
		return BitcoinClient().getconnectioncount

