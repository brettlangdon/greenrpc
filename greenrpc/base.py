import time
import types

import msgpack


class BaseServer(object):
    SOCKET_BUFFER_SIZE = 1024

    def __init__(self, services):
        if isinstance(services, (dict, types.ModuleType)):
            self.services = services
        elif isinstance(services, basestring):
            self.services = __import__(services)
        else:
            raise TypeError("First argument to BaseServer.__init__ must be a dict or a string")

        self.packer = msgpack.Packer()

    def unpack_requests(self, sock):
        unpacker = msgpack.Unpacker()
        while True:
            data = sock.recv(self.SOCKET_BUFFER_SIZE)
            if not data:
                break
            unpacker.feed(data)
            for request in unpacker:
                yield request

    def pack_result(self, result):
        return self.packer.pack(result)

    def handle_request(self, request):
        start_time = time.time()
        req_method = request.get("method")
        req_args = request.get("args", [])

        result = {
            "id": request.get("id"),
            "results": None,
        }

        if not req_method:
            result["error"] = "No request method was provided"
        elif not hasattr(self.services, req_method):
            result["error"] = "Unknown request method '%s'" % (req_method, )
        else:
            try:
                result["results"] = getattr(self.services, req_method)(*req_args)
            except Exception, e:
                result["error"] = e.message

        result["run_time"] = (time.time() - start_time) * 1000.0
        return result


class BaseClient(object):
    SOCKET_BUFFER_SIZE = 1024

    def __init__(self):
        self.unpacker = msgpack.Unpacker()
        self.packer = msgpack.Packer()
        self.id = 0

    def pack_request(self, id, method, args=[]):
        return self.packer.pack({
            "id": id,
            "method": method,
            "args": args,
        })

    def unpack_results(self, sock):
        while True:
            data = sock.recv(self.SOCKET_BUFFER_SIZE)
            if not data:
                break
            self.unpacker.feed(data)
            return self.unpacker.next()

    def __getattr__(self, method):
        def wrapper(*args):
            return self.call(method, args)
        return wrapper
