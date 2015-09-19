import unittest

import redis_commands
from tests.unit.stubs import ConnectionStub


class TestRedisCommands(unittest.TestCase):
    def test_info(self):
        conn_stub = ConnectionStub()
        _, message = redis_commands.info(conn_stub, None)
        self.assertEquals(message, "+Functional Python Redis Server running on 127.0.0.1 port 6379 \r\n")

    def test_set_key(self):
        hashmap = {}
        resulting_hashmap, _ = redis_commands.set(None, hashmap, "key", "1")
        self.assertEquals(resulting_hashmap.get("key"), "1")
        self.assertIsNot(hashmap, resulting_hashmap)

    def test_get_key(self):
        hashmap = {"key": "1"}
        _, resulting_value = redis_commands.get(None, hashmap, "key")
        self.assertEquals(resulting_value, "$1\r\n1\r\n")

    def test_find_commands(self):
        self.assertEquals(redis_commands.find("set"), redis_commands.set)
        self.assertEquals(redis_commands.find("get"), redis_commands.get)
        self.assertEquals(redis_commands.find("info"), redis_commands.info)
        self.assertEquals(
            redis_commands.find("invalid").func_name, redis_commands._command_not_found("invalid").func_name)


class TestParseCommandStrings(unittest.TestCase):
    def test_discard_protocol_labels(self):
        params = ['*3', '$3', 'SET', '$3', 'key', '$1', "'Hello'"]
        self.assertEquals(["SET", "key", "'Hello'"], redis_commands.discard_protocol_labels(params))

    def test_parse_set_command(self):
        received_data = "*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$1\r\n'Hello'\r\n"
        command, params = redis_commands.parse(received_data)
        self.assertEquals(command, "set")
        self.assertEquals(params, ("key", "Hello"))
