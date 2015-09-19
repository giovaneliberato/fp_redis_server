

class SocketStub:
    def __init__(self):
        self.bound = False
        self.address = ()
        self.listening = False
        self.received = False
        self.data = None
        self.accepting = False

    def bind(self, address):
        self.address = address
        self.bound = True

    def listen(self, max_connections):
        self.listening = True

    def recv(self, bytes):
        self.received = True
        return "data"

    def accept(self):
        self.accepting = True
        return None, None


class ConnectionStub:
    def __init__(self):
        self.sent_message = None

    def sendall(self, message):
        self.sent_message = message

    def getsockname(self):
        return "127.0.0.1", 6379
