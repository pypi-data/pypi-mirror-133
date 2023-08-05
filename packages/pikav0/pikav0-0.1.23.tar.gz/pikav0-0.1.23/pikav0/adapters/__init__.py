"""
Connection Adapters
===================

Pika provides multiple adapters to connect to RabbitMQ:

- adapters.asyncio_connection.AsyncioConnection: Native Python3 AsyncIO use
- adapters.blocking_connection.BlockingConnection: Enables blocking,
  synchronous operation on top of library for simple uses.
- adapters.select_connection.SelectConnection: A native event based connection
  adapter that implements select, kqueue, poll and epoll.
- adapters.tornado_connection.TornadoConnection: Connection adapter for use
  with the Tornado web framework.
- adapters.twisted_connection.TwistedConnection: Connection adapter for use
  with the Twisted framework

"""
from pikav0.adapters.base_connection import BaseConnection
from pikav0.adapters.blocking_connection import BlockingConnection
from pikav0.adapters.select_connection import SelectConnection
from pikav0.adapters.select_connection import IOLoop

# Dynamically handle 3rd party library dependencies for optional imports
try:
    from pikav0.adapters.asyncio_connection import AsyncioConnection
except ImportError:
    AsyncioConnection = None

try:
    from pikav0.adapters.tornado_connection import TornadoConnection
except ImportError:
    TornadoConnection = None

try:
    from pikav0.adapters.twisted_connection import TwistedConnection
    from pikav0.adapters.twisted_connection import TwistedProtocolConnection
except ImportError:
    TwistedConnection = None
    TwistedProtocolConnection = None

