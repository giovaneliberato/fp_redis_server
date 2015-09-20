import socket
import redis_commands

SERVER_ADDRESS = ("127.0.0.1", 6379)
BYTES_LENGTH = 1024


def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def listen(sock, server_address):
    sock.bind(server_address)
    sock.listen(1)
    return sock


def accept(sock):
    conn, client_address = sock.accept()
    return conn, client_address


def receive_data(conn):
    return conn.recv(BYTES_LENGTH)


def execute_command(conn, hashmap):
    command, params = redis_commands.parse(receive_data(conn))
    command_fn = redis_commands.find(command)
    hashmap, response = command_fn(conn, hashmap, *params)
    conn.sendall(response)
    print("--- Received command: %s" % command.upper())
    execute_command(conn, hashmap)


def start(server_address):
    hashmap = {}

    print("--- Starting Redis server at %s %d" % server_address)
    conn, client_address = accept(listen(create_socket(), server_address))
    print("--- Client %s %d connected" % client_address)
    try:
        execute_command(conn, hashmap)
    except Exception as e:
        print("--- Unknown error: %s" % e.message)
        conn.close()

if __name__ == "__main__":
    start(SERVER_ADDRESS)
