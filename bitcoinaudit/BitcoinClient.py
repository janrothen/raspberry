from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from utils.config import config

RPC_IP = config().get('bitcoin.rpc', 'ip')
RPC_PORT = int(config().get('bitcoin.rpc', 'port'))
RPC_USER = config().get('bitcoin.rpc', 'user')
RPC_PASSWORD = config().get('bitcoin.rpc', 'password')
RPC_TIMEOUT = int(config().get('bitcoin.rpc', 'timeout'))

def lazy_property(fn):
    '''Decorator that makes a property lazy-evaluated.
    '''
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

class BitcoinClient(object):

    @lazy_property
    def get_cached_txoutsetinfo(self):
        info = self.get_gettxoutsetinfo()
        return info

    def get_gettxoutsetinfo(self):
        return self.get_connection().gettxoutsetinfo()

    def get_getconnectioncount(self):
        return self.get_connection().getconnectioncount()

    def get_connection(self):
        connection_string = f'http://{RPC_USER}:{RPC_PASSWORD}@{RPC_IP}:{RPC_PORT}'
        return AuthServiceProxy(connection_string, timeout=RPC_TIMEOUT)

    def get_block_height(self):
        return self.get_cached_txoutsetinfo['height']
    
    def get_total_amount(self):
        return self.get_cached_txoutsetinfo['total_amount']

    def get_connection_count(self):
        return self.get_getconnectioncount()