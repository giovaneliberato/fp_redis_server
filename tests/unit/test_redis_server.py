import socket
import unittest

from mockito import when

import redis_server
from tests.unit.stubs import SocketStub


class TestRedisConnection(unittest.TestCase):
    SERVER_ADDRESS = ("127.0.0.1", 6379)

    def test_create_socket(self):
        socket_stub = SocketStub()
        when(socket).socket(socket.AF_INET, socket.SOCK_STREAM).thenReturn(socket_stub)
        result = redis_server.create_socket()
        self.assertEquals(socket_stub, result)

    def test_listen_to_port(self):
        socket_stub = SocketStub()
        redis_server.listen(socket_stub, self.SERVER_ADDRESS)
        self.assertTrue(socket_stub.bound)
        self.assertEquals(self.SERVER_ADDRESS, socket_stub.address)
        self.assertTrue(socket_stub.listening)

    def test_accept_connections(self):
        socket_stub = SocketStub()
        redis_server.accept(socket_stub)
        self.assertTrue(socket_stub.accepting)

    def test_data_receive(self):
        socket_stub = SocketStub()
        data = redis_server.receive_data(socket_stub)
        self.assertTrue(socket_stub.received)
        self.assertEquals(data, "data")


if __name__ == '__main__':
    unittest.main()
