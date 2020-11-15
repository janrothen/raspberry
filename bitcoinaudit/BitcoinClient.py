from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from utils.config import config

RPC_IP = config().get('bitcoin.rpc', 'ip')
RPC_PORT = int(config().get('bitcoin.rpc', 'port'))
RPC_USER = config().get('bitcoin.rpc', 'user')
RPC_PASSWORD = config().get('bitcoin.rpc', 'password')
RPC_TIMEOUT = int(config().get('bitcoin.rpc', 'timeout'))

class BitcoinClient(object):

    @property
    def gettxoutsetinfo(self):
        try:
            return self.value
        except AttributeError:
            self.value = self.get_connection().gettxoutsetinfo()
            return self.value

    @property
    def getconnectioncount(self):
        return self.get_connection().getconnectioncount()

    def get_connection(self):
        connection_string = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_IP}:{RPC_PORT}'
        return AuthServiceProxy(connection_string, timeout=RPC_TIMEOUT)

    def get_block_height(self):
        return BitcoinClient().gettxoutsetinfo['height']
    
    def get_total_amount(self):
        return BitcoinClient().gettxoutsetinfo['total_amount']

    def get_connection_count(self):
        return BitcoinClient().getconnectioncount