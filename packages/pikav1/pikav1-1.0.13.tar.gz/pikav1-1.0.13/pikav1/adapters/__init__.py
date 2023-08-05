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
- adapters.twisted_connection.TwistedProtocolConnection: Connection adapter for use
  with the Twisted framework

"""
from pikav1.adapters.base_connection import BaseConnection
from pikav1.adapters.blocking_connection import BlockingConnection
from pikav1.adapters.select_connection import SelectConnection
from pikav1.adapters.select_connection import IOLoop
