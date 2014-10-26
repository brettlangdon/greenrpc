from gevent.socket import socket

from greenrpc import TCP_SERVER_DEFAULT_PORT
from greenrpc.base import BaseClient
from greenrpc.error import RPCException


class TCPClient(BaseClient):
    def __init__(self, connect=("127.0.0.1", TCP_SERVER_DEFAULT_PORT)):
        super(TCPClient, self).__init__()
        self.connection = socket()
        self.connection.connect(connect)
        self.fp = self.connection.makefile()

    def call(self, method, args=[], debug=False):
        self.id += 1
        request = self.pack_request(self.id, method, args)
        self.fp.write(request)
        self.fp.flush()
        results = self.unpack_results(self.connection)
        if debug:
            return results
        if results.get("error"):
            raise RPCException(results["error"])
        return results.get("results")


class HTTPClient(BaseClient):
    pass
