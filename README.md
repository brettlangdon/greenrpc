GreenRPC
========

TCP & HTTP RPC Server written with [msgpack](http://msgpack.org/) and
[gevent](http://www.gevent.org/)

## Install
### pip

```bash
pip install greenrpc
```

### git
```bash
git clone git://github.com/brettlangdon/greenrpc.git
cd ./greenrpc
python setup.py install
```


## Usage
### server
```bash
$ greenrpc-server -h
usage: greenrpc-server [-h] [--bind BIND] [--spawn SPAWN] [--http] <module> [<module> ...]

Start a new GreenRPC TCP Server

positional arguments:
<module>       Python module to expose for the RPC Server

optional arguments:
-h, --help     show this help message and exit
--bind BIND    <address>:<port> to bind the server to (default: 127.0.0.1:3434)
--spawn SPAWN  number of greenlets to spawn (default: 4)
--http         whether to start an http server instead of tcp (default: False)
```

Expose the python module [time](https://docs.python.org/2/library/time.html) as
an RPC server
```
$ greenrpc-server time
```

Exposing multiple modules
```
$ greenrpc-server time json
```

### cli client
```bash
$ greenrpc-client -h
usage: greenrpc-client [-h] [--connect CONNECT] [--debug] [--http] <method> [<arg> [<arg> ...]]

Start a new GreenRPC TCP Server

positional arguments:
<method>           The remote method to call
<arg>              Arguments to send for the remote method call

optional arguments:
-h, --help         show this help message and exit
--connect CONNECT  <address>:<port> of the server to connect to(default: 127.0.0.1:3434)
--debug            whether or not to show the full result
--http             whether the server is http or tcp
```

```
$ greenrpc-client time
1414368752.71
$ greenrpc-client --debug time
{'results': 1414368766.407974, 'run_time': 0.0059604644775390625, 'id': 1}
```

### python client
```python
from greenrpc.client import TCPClient

client = TCPClient()
print client.time()
# 1414368818.587777
print client.call("time")
# 1414368830.217749
print client.call("time", debug=True)
# {'results': 1414368849.379209, 'run_time': 0.008106231689453125, 'id': 3}
```


## License
```
The MIT License (MIT)

Copyright (c) 2014 Brett Langdon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
