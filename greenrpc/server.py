import contextlib

from gevent.pywsgi import WSGIServer
from gevent.server import StreamServer

from greenrpc import TCP_SERVER_DEFAULT_PORT, HTTP_SERVER_DEFAULT_PORT
from greenrpc.base import BaseServer


class TCPServer(StreamServer, BaseServer):
    def __init__(self, services, bind=("127.0.0.1", TCP_SERVER_DEFAULT_PORT), spawn=1):
        StreamServer.__init__(self, bind, spawn=spawn)
        BaseServer.__init__(self, services)

    def handle(self, socket, address):
        with contextlib.closing(socket) as sock:
            with contextlib.closing(sock.makefile()) as fp:
                for request in self.unpack_requests(sock):
                    result = self.handle_request(request)
                    fp.write(self.pack_result(result))
                    fp.flush()


class WSGIServer(WSGIServer, BaseServer):
    def __init__(self, services, bind=("127.0.0.1", HTTP_SERVER_DEFAULT_PORT)):
        WSGIServer.__init__(self, bind)
        BaseServer.__init__(self, services)

    def application(self, environ, start_response):
        start_response("200 OK", [("Content-Type", "text/plain")])
        return ["Hello, Worlds"]
