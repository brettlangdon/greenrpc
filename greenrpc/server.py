import contextlib
import json
import urlparse

from gevent import pywsgi
from gevent.server import StreamServer
import msgpack

from greenrpc import DEFAULT_PORT
from greenrpc.base import BaseServer


class TCPServer(StreamServer, BaseServer):
    def __init__(self, services, bind=("127.0.0.1", DEFAULT_PORT), spawn=1):
        StreamServer.__init__(self, bind, spawn=spawn)
        BaseServer.__init__(self, services)

    def handle(self, socket, address):
        with contextlib.closing(socket) as sock:
            with contextlib.closing(sock.makefile()) as fp:
                for request in self.unpack_requests(sock):
                    result = self.handle_request(request)
                    fp.write(self.pack_result(result))
                    fp.flush()


class WSGIServer(pywsgi.WSGIServer, BaseServer):
    def __init__(self, services, bind=("127.0.0.1", DEFAULT_PORT), spawn=1):
        pywsgi.WSGIServer.__init__(self, bind, spawn=spawn)
        BaseServer.__init__(self, services)

    def decode(self, decoder, data):
        decoder = decoder.lower()
        if decoder == "json":
            return json.loads(data)
        elif decoder == "msgpack":
            return msgpack.unpackb(data)

    def encode(self, encoder, data):
        encoder = encoder.lower()
        if encoder == "json":
            return json.dumps(data)
        elif encoder == "msgpack":
            return msgpack.packb(data)

    def content_type(self, encoder):
        encoder = encoder.lower()
        mime = "text/plain"
        if encoder == "json":
            mime = "application/json"
        elif encoder == "msgpack":
            mime = "application/x-msgpack"
        return ("Content-Type", mime)

    def application(self, environ, start_response):
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        uri = environ["PATH_INFO"]
        uri = uri.strip("/")
        encoder, _, method = uri.partition("/")

        qs = urlparse.parse_qs(environ["QUERY_STRING"])
        request = {
            "id": qs.get("id", [None])[0],
            "args": qs.get("arg", []),
            "method": method,
        }

        if environ["REQUEST_METHOD"] == "POST":
            data = environ["wsgi.input"].read(content_length)
            data = self.decode(encoder, data)
            request["method"] = data.get("method", request["method"])
            request["args"] = data.get("args", request["args"])
            request["id"] = data.get("id", request["id"])

        result = self.handle_request(request)
        start_response("200 OK", [self.content_type(encoder)])
        return [self.encode(encoder, result)]
